"""
Represents a circle object with properties and methods for managing its data.

This class is used to represent a circle identified in a video frame. It stores
information about the circle's center location (x, y), radius, color, and
optionally tracks the circle across multiple frames (data list).
"""

import os
import math
import json
import numpy as np

from app.logging_config import logger


class Circle:
    """
    Represents a circle object with properties and methods for managing its data.

    Attributes:
        x (int): x-coordinate of the circle's center.
        y (int): y-coordinate of the circle's center.
        radius (int): Radius of the circle.
        color (tuple): Color of the circle (represented as a tuple of floats, likely RGB values).
        frame (int): Frame number associated with the circle data.
        data (list): A list of dictionaries containing information about the circle at different frames (includes x, y, frame, radius, color, and distance).
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        radius: int = 0,
        color: tuple = None,
        frame: int = 0,
        video_height: int = 0,
    ):
        """
        Initializes a Circle object.

        Args:
            x (int, optional): x-coordinate of the circle's center. Defaults to 0.
            y (int, optional): y-coordinate of the circle's center. Defaults to 0.
            radius (int, optional): Radius of the circle. Defaults to 0.
            color (tuple, optional): Color of the circle (represented as a tuple of floats, likely RGB values). Defaults to None.
            frame (int, optional): Frame number associated with the circle data. Defaults to 0.
            video_height (int, optional): The height of the video frame to calculate the y-coordinate relative to the bottom of the frame. Defaults to 0.
        """
        self.x = int(x)
        self.y = int(y)
        self.frame = int(frame)
        self.radius = int(radius)
        self.color = Circle.filter_nan(color)
        self.data = [
            {
                "x": self.x,
                "y": (video_height - self.y),
                "frame": frame,
                "radius": self.radius,
                "color": self.color,
            }
        ]

    @staticmethod
    def filter_nan(color: tuple) -> tuple:
        """
        Filters out NaN values and keeps only valid floating-point numbers.

        Args:
            color (Optional[List[float]]): A list of values, potentially containing NaN values.

        Returns:
            Optional[List[float]]: A new list containing only the valid floating-point numbers from the input,
                                   or None if all values are NaN.
        """
        filtered_color = []
        for x in color:
            if not isinstance(x, float) or math.isnan(x):
                return None
            filtered_color.append(x)

        return tuple(filtered_color)

    @staticmethod
    def is_valid_color(color: tuple[float, float, float]) -> bool:
        """
        Validates if a color is a valid RGB tuple.

        Args:
            color (Tuple[float, float, float]): The RGB color tuple to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return (
            isinstance(color, tuple)
            and len(color) == 3
            and all(isinstance(c, float) and 0 <= c <= 255 for c in color)
        )

    @staticmethod
    def are_colors_similar(
        color1: tuple[float, float, float],
        color2: tuple[float, float, float],
        tolerance: int = 30,
    ) -> bool:
        """
        Compares the similarity of two RGB colors with a specified tolerance.

        Args:
            color1 (Tuple[float, float, float]): The first RGB color as a tuple (R, G, B) with values ranging from 0 to 255.
            color2 (Tuple[float, float, float]): The second RGB color as a tuple (R, G, B) with values ranging from 0 to 255.
            tolerance (int, optional): The maximum allowed difference for each color component (R, G, B). Defaults to 30.

        Returns:
            Optional[bool]: True if the colors are considered similar within the specified tolerance, False otherwise.
                            None if either color1 or color2 is invalid.
        """
        if not (Circle.is_valid_color(color1) and Circle.is_valid_color(color2)):
            return None

        color_diffs = np.abs(np.array(color1) - np.array(color2))
        return np.all(color_diffs <= tolerance)

    def are_circles_same(
        self, circle: "Circle", distance_threshold: int = 50, radius_threshold: int = 17
    ):
        """
        Checks if two circles are the same based on distance and radius.

        Args:
            circle (Circle): The other circle to compare to.
            distance_threshold (int, optional): The maximum distance between the centers of the circles
                                                for them to be considered the same. Defaults to 50.
            radius_threshold (int, optional): The maximum difference in radius between the circles
                                              for them to be considered the same. Defaults to 17.

        Returns:
            Union[float, bool]: The distance between the circles if they are considered the same, False otherwise.
        """
        distance = np.sqrt((circle.x - self.x) ** 2 + (circle.y - self.y) ** 2)
        radius_diff = abs(circle.radius - self.radius)

        if distance <= distance_threshold and radius_diff <= radius_threshold:
            return distance
        return False

    def same_circle(self, circle: "Circle", video_height: int) -> bool:
        """
        Updates current circle's data if it matches with another circle.

        Args:
            circle (Circle): The circle object to compare with the calling circle.
            video_height (int): The height of the video frame to calculate the y-coordinate relative to the bottom of the frame.

        Returns:
            bool: True if the circles are considered the same and the calling circle's data is updated, False otherwise.
        """
        if circle.frame <= self.frame:
            return False

        if (circle.frame - self.frame) > 20:
            return False

        distance = self.are_circles_same(circle)
        if distance is False:
            return False

        if Circle.are_colors_similar(self.color, circle.color) is False:
            return False

        self.x, self.y, self.frame = circle.x, circle.y, circle.frame
        self.data.append(
            {
                "x": circle.x,
                "y": (video_height - circle.y),
                "frame": circle.frame,
                "radius": circle.radius,
                "distance": distance,
                "color": circle.color,
            }
        )

        return True

    def save_circle(self, name: int = 0) -> None:
        """
        Saves the circle's data as a JSON file.

        Args:
            name (int, optional): An optional integer to append to the filename. Defaults to 0.
        """
        filename = f"circle_data_{name}.json"

        circle_data = {
            "filename": filename,
            "radius": self.radius,
            "color": self.color,
            "data": self.data,
        }

        try:
            os.makedirs("data", exist_ok=True)
            data_file = os.path.join("data", filename)
            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(circle_data, file, indent=4)
            logger.info("Saved data for circle in: %s", filename)
        except Exception as e:
            logger.error("Failed to save circle data: %s", e)


# Example usage of the Circle class
if __name__ == "__main__":
    # Initialize a circle
    circle1 = Circle(
        x=100, y=200, radius=50, color=(255.0, 0.0, 0.0), frame=1, video_height=1080
    )
    circle2 = Circle(
        x=105, y=205, radius=50, color=(255.0, 0.0, 0.0), frame=2, video_height=1080
    )

    # Check if circle2 is the same as circle1
    same = circle1.same_circle(circle2, video_height=1080)
    print(f"Circles are the same: {same}")

    # Save circle data to a file
    circle1.save_circle(name=1)
