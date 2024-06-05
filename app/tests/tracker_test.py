import os
import pytest
import cv2
import numpy as np
from unittest.mock import patch, MagicMock

from app.tracker import Tracker
from app.circle import Circle
from app.rectangle import Rectangle


# Sample video frame for testing
def generate_test_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(frame, (320, 240), 50, (255, 255, 255), -1)  # White circle
    cv2.rectangle(frame, (100, 100, 50, 50), (255, 255, 255), -1)  # White square
    return frame


@pytest.fixture
def tracker():
    return Tracker()


@pytest.fixture
def sample_frame():
    return generate_test_frame()


def test_load_video_failure(tracker):
    with patch("cv2.VideoCapture") as mock_video:
        mock_video.return_value.isOpened.return_value = False
        with pytest.raises(FileNotFoundError):
            tracker.load_video()


def test_process_circles(tracker, sample_frame):
    frame_grayscale = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2GRAY)
    tracker.process_circles(frame_grayscale, sample_frame, 1)
    assert len(tracker.circles) > 0
    assert isinstance(tracker.circles[0], Circle)


def test_process_rectangles(tracker, sample_frame):
    frame_grayscale = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2GRAY)
    tracker.process_rectangles(frame_grayscale, sample_frame, 1)
    assert len(tracker.rectangles) > 0
    assert isinstance(tracker.rectangles[0], Rectangle)


def test_delete_dir(tracker, tmp_path):
    dir_path = tmp_path / "data"
    dir_path.mkdir()
    (dir_path / "circle_data_test.txt").write_text("test")
    (dir_path / "rectangle_data_test.txt").write_text("test")
    (dir_path / "other_file.txt").write_text("test")

    tracker.delete_dir(dir_name=dir_path)
    assert not (dir_path / "circle_data_test.txt").exists()
    assert not (dir_path / "rectangle_data_test.txt").exists()
    assert (dir_path / "other_file.txt").exists()


def test_track(tracker):
    # Mock methods for testing
    with patch.object(tracker, "delete_dir") as mock_delete_dir, patch.object(
        tracker, "load_video"
    ) as mock_load_video, patch.object(
        tracker, "process_circles"
    ) as mock_process_circles, patch.object(
        tracker, "process_rectangles"
    ) as mock_process_rectangles, patch(
        "cv2.VideoCapture"
    ) as mock_video_capture, patch(
        "cv2.imshow"
    ), patch(
        "cv2.waitKey", return_value=ord("q")
    ):

        mock_video = MagicMock()
        mock_video.isOpened.side_effect = [True, False]
        mock_video.read.side_effect = [(True, generate_test_frame()), (False, None)]
        mock_video_capture.return_value = mock_video

        tracker.track()

        mock_delete_dir.assert_called_once()
        mock_load_video.assert_called_once()
        # mock_process_circles.assert_called()
        # mock_process_rectangles.assert_called()
        # mock_video_capture.return_value.release.assert_called_once()
        # cv2.destroyAllWindows.assert_called_once()


if __name__ == "__main__":
    pytest.main()
