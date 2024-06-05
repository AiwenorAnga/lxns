"""
This program tracks circles and rectangles in a video using OpenCV.
The processed data are stored in the data dir.

Dependencies:
    - OpenCV (cv2)
    - NumPy (np)

Classes:
    - Tracker: Class to track circles and rectangles in a video.

Functions:
    - __init__: Initializes the Tracker with dictionaries for circles and rectangles.
    - load_video: Loads the video file.
    - process_circles: Processes circles in the frame.
    - process_rectangles: Processes rectangles in the frame.
    - track: Tracks circles and rectangles in the video.

Usage:
    - Create an instance of Tracker.
    - Call the track method to start tracking circles and rectangles in the video.
"""

import os
import cv2
import numpy as np

from app.circle import Circle
from app.rectangle import Rectangle
from app.logging_config import logger


class Tracker:
    """Class to track circles and rectangles in a video."""

    def __init__(self):
        """Initialize the Tracker with dictionaries for circles and rectangles."""
        self.circles = []
        self.rectangles = []
        self.video_height = 0
        self.video_width = 0

    def delete_dir(self, dir_name="data"):
        for filename in os.listdir(dir_name):
            file_path = os.path.join(dir_name, filename)
            if (
                os.path.isfile(file_path)
                and "circle_data_" in filename
                or "rectangle_data_" in filename
            ):
                os.remove(file_path)

    def delete_dir(self, dir_name="data"):
        """
        Deletes files containing "circle_data_" or "rectangle_data_" in their names
        from the specified directory.

        Args:
            dir_name (str, optional): The directory path to delete files from. Defaults to "data".

        Raises:
            OSError: If the directory path is invalid or there's an error during deletion.
        """

        if not os.path.isdir(dir_name):
            logger.info("Directory not found: %s", dir_name)
            try:
                os.makedirs(dir_name)
                logger.info("Directory '%s' created successfully.", dir_name)
            except OSError as e:
                logger.error("Error creating directory '%s': %s", dir_name, e)

        for filename in os.listdir(dir_name):
            file_path = os.path.join(dir_name, filename)
            if os.path.isfile(file_path):
                if "circle_data_" in filename or "rectangle_data_" in filename:
                    try:
                        os.remove(file_path)
                        logger.info("Deleted file: %s/%s", dir_name, filename)
                    except OSError as e:
                        logger.error(
                            "Failed to delete the file: %s/%s %s", dir_name, filename, e
                        )

    def load_video(self):
        """
        Load the video file.

        Returns:
            video (cv2.VideoCapture): The video capture object.
        """
        video = cv2.VideoCapture("luxonis_task_video.mp4")
        if not video.isOpened():
            logger.error("Error opening video file.")
            raise FileNotFoundError("Video file cannot be opened.")

        self.video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return video

    def process_circles(self, frame_grayscale, frame, frame_counter: int) -> None:
        """
        Detect circles in a video frame and update the circle's list.

        Args:
            frame_grayscale (np.ndarray): The grayscale frame.
            frame (np.ndarray): The RGB frame.
            frame_counter (int): The frame number.
        """
        circles = cv2.HoughCircles(
            frame_grayscale,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=50,
            param1=50,
            param2=30,
            minRadius=10,
            maxRadius=100,
        )
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for x, y, r in circles:
                if (
                    y - r >= 0
                    and y + r < frame.shape[0]
                    and x - r >= 0
                    and x + r < frame.shape[1]
                ):
                    circle_region = frame[y - r : y + r, x - r : x + r]
                    if circle_region.size > 0:  # Check if region is not empty
                        average_color = np.mean(circle_region, axis=(0, 1))
                        average_color = tuple([x for x in average_color[::-1]])
                        cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

                        new_circle = Circle(
                            x,
                            y,
                            r,
                            average_color,
                            frame_counter,
                            self.video_height,
                        )

                        if not any(
                            circle.same_circle(new_circle, self.video_height)
                            for circle in self.circles
                        ):
                            self.circles.append(new_circle)
                            logger.info(
                                "New circle detected: x:%s y:%s rad:%s frame:%s",
                                new_circle.x,
                                new_circle.y,
                                new_circle.radius,
                                new_circle.frame,
                            )

    def process_rectangles(self, frame_grayscale, frame, frame_counter: int) -> None:
        """
        Detect rectangles in a video frame and update the rectangle's list.

        Args:
            frame_grayscale (numpy.ndarray): Grayscale frame.
            frame (numpy.ndarray): Original frame.
            frame_counter (int): Frame number.

        """
        thresh = cv2.threshold(frame_grayscale, 10, 555, cv2.THRESH_BINARY)[1]

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        rectangles = []
        for contour in contours:
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True
            )
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if w == h:
                    center_x, center_y = x + w // 2, y + h // 2
                    color = frame[center_y, center_x]
                    color = tuple([float(x) for x in color])
                    rectangles.append((x, y, w, h, color))

        for x, y, w, h, color in rectangles:
            new_rectangle = Rectangle(
                x, y, w, h, color, frame_counter, self.video_height
            )

            if w is not h:
                continue

            is_new_rectangle = True
            for rectangle in self.rectangles:
                if rectangle.same_rectangle(new_rectangle, self.video_height):
                    is_new_rectangle = False
                    break
            if is_new_rectangle:
                self.rectangles.append(new_rectangle)
                logger.info(
                    "New rectangle detected: x:%s y:%s w:%s h:%s frame:%s",
                    new_rectangle.x,
                    new_rectangle.y,
                    new_rectangle.width,
                    new_rectangle.height,
                    new_rectangle.frame,
                )

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (x + w // 2, y + h // 2), 2, (255, 0, 0), 3)

    def track(self) -> None:
        """Track circles and rectangles in the video."""
        frame_counter = 0
        self.delete_dir()
        video = self.load_video()

        while video.isOpened() and frame_counter < 1000:
            frame_counter += 1
            try:
                ret, frame = video.read()
            except ValueError:
                logger.warning("Frame %s could not be read.", frame_counter)
                break
            if not ret:
                logger.warning("Frame %s could not be read.", frame_counter)
                break
            frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.process_circles(frame_grayscale, frame, frame_counter)
            self.process_rectangles(frame_grayscale, frame, frame_counter)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video.release()
        cv2.destroyAllWindows()

        x = 0
        for circle in self.circles:
            x += 1
            circle.save_circle(x)
        x = 0
        for rectangle in self.rectangles:
            x += 1
            rectangle.save_rectangle(x)

        logger.info("Circles detected:%s", len(self.circles))
        logger.info("Rectangle detected:%s", len(self.rectangles))
        logger.info("Tracking completed and data saved.")


if __name__ == "__main__":
    tracker = Tracker()
    tracker.track()
