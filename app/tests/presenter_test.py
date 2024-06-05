import pytest
import json
import os
from unittest import mock
from tkinter import filedialog
from app.presenter import Presenter


# Helper function to create a mock JSON file
def create_mock_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)


def test_load_json_files(monkeypatch):
    mock_file_paths = ["test_data_1.json", "test_data_2.json"]
    mock_data = [{"data": [{"x": 1, "y": 2, "frame": 1}, {"x": 3, "y": 4, "frame": 2}]}]
    for file_path in mock_file_paths:
        create_mock_json_file(file_path, mock_data[0])
    monkeypatch.setattr(filedialog, "askopenfilenames", lambda **args: mock_file_paths)
    presenter = Presenter()
    data, filenames = presenter.load_json_files()

    assert len(data) == 2
    assert len(filenames) == 2
    assert data[0] == mock_data[0]["data"]
    assert data[1] == mock_data[0]["data"]

    for file_path in mock_file_paths:
        os.remove(file_path)


def test_update():
    presenter = Presenter()
    presenter.x_coords_list = [[1, 2, 3], [4, 5, 6]]
    presenter.y_coords_list = [[2, 3, 4], [5, 6, 7]]
    presenter.filenames = ["file1.json", "file2.json"]
    presenter.min_frame = 1
    presenter.max_x = 10
    presenter.max_y = 10

    with mock.patch("matplotlib.pyplot.plot") as mock_plot, mock.patch(
        "matplotlib.pyplot.cla"
    ), mock.patch("matplotlib.pyplot.xlabel"), mock.patch(
        "matplotlib.pyplot.ylabel"
    ), mock.patch(
        "matplotlib.pyplot.title"
    ), mock.patch(
        "matplotlib.pyplot.gca"
    ), mock.patch(
        "matplotlib.pyplot.xlim"
    ), mock.patch(
        "matplotlib.pyplot.ylim"
    ), mock.patch(
        "matplotlib.pyplot.legend"
    ), mock.patch(
        "matplotlib.pyplot.grid"
    ):

        presenter.update(2)
        assert mock_plot.called
        assert mock_plot.call_count == 2


def test_on_key_press():
    presenter = Presenter()
    event = mock.Mock()
    event.key = "enter"
    with mock.patch("matplotlib.pyplot.close") as mock_close, mock.patch(
        "sys.exit"
    ) as mock_exit:
        presenter.on_key_press(event)
        mock_close.assert_called_once()
        mock_exit.assert_called_once_with(0)


def test_present(monkeypatch):
    mock_file_paths = ["test_data_1.json"]
    mock_data = [{"data": [{"x": 1, "y": 2, "frame": 1}, {"x": 3, "y": 4, "frame": 2}]}]
    create_mock_json_file(mock_file_paths[0], mock_data[0])
    monkeypatch.setattr(filedialog, "askopenfilenames", lambda **args: mock_file_paths)

    presenter = Presenter()

    with mock.patch("matplotlib.pyplot.show"), mock.patch(
        "matplotlib.pyplot.figure"
    ), mock.patch("matplotlib.pyplot.grid"), mock.patch(
        "matplotlib.animation.FuncAnimation"
    ) as mock_animation:

        presenter.present()
        assert presenter.filenames == ["test_data_1.json"]
        assert presenter.min_frame == 1
        assert presenter.max_frame == 2
        assert presenter.max_x == 3
        assert presenter.max_y == 4
        assert mock_animation.called

    os.remove(mock_file_paths[0])


if __name__ == "__main__":
    pytest.main()
