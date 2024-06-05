"""A class representing a rectangle with properties and methods to handle
    rectangle data, including position, size, color, and frame information.
"""

import os
import json
import numpy as np

from app.circle import Circle
from app.logging_config import logger


class Rectangle(Circle):
    """A class representing a rectangle with properties and methods to handle
    rectangle data, including position, size, color, and frame information.

    Attributes:
        x (int): x-coordinate of the rectangle's center.
        y (int): y-coordinate of the rectangle's center.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        color (tuple): The color of the rectangle in RGB format.
        frame (int): Frame number associated with the rectangle data.
        data (list): A list of dictionaries containing information about the rectangle at different frames (includes x, y, frame, width, height, color, and distance).
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        color: tuple = None,
        frame: int = 0,
        video_height=0,
    ):
        """Initializes a Rectangle object with position, size, color, and frame data.

        Args:
            x (int): The x-coordinate of the rectangle. Defaults to 0.
            y (int): The y-coordinate of the rectangle. Defaults to 0.
            width (int): The width of the rectangle. Defaults to 0.
            height (int): The height of the rectangle. Defaults to 0.
            color (tuple): The color of the rectangle in RGB format. Defaults to None.
            frame (int): The frame number associated with the rectangle. Defaults to 0.
            video_height (int): The height of the video frame for coordinate transformation. Defaults to 0.
        """
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.frame = int(frame)
        self.color = self.filter_nan(color)
        self.data = [
            {
                "x": self.x,
                "y": (video_height - self.y),
                "width": self.width,
                "height": self.height,
                "frame": frame,
                "color": self.color,
            }
        ]

    def are_rectangles_same(
        self,
        rect: "Rectangle",
        distance_threshold: int = 40,
        size_diff_threshold: int = 5,
    ):
        """Determines if two rectangles are considered the same based on distance and size.

        Args:
            rect (Rectangle): Another rectangle object to compare with.
            distance_threshold (int, optional): The maximum allowed distance between the centers of the rectangles. Defaults to 40.
            size_diff_threshold (int, optional): The maximum allowed size difference for width and height. Defaults to 5.

        Returns:
            float: The distance between the centers of the rectangles if they are considered the same.
            bool: False if the rectangles are not considered the same.
        """
        x1, y1, w1, h1 = (self.x, self.y, self.width, self.height)
        x2, y2, w2, h2 = (rect.x, rect.y, rect.width, rect.height)

        center1 = (x1 + w1 // 2, y1 + h1 // 2)
        center2 = (x2 + w2 // 2, y2 + h2 // 2)

        distance = np.sqrt(
            (center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2
        )
        size_diff = max(abs(w1 - w2), abs(h1 - h2))

        if distance <= distance_threshold and size_diff <= size_diff_threshold:
            return distance
        else:
            return False

    def same_rectangle(self, rectangle: "Rectangle", video_height: int) -> bool:
        """Updates current rectangle's data if it matches with another rectangle.

        Args:
            rectangle (Rectangle): Another rectangle object to compare with.
            video_height (int): The height of the video frame for coordinate transformation.

        Returns:
            bool: True if the rectangle was updated with new data, False otherwise.
        """

        if rectangle.frame <= self.frame:
            return False

        if (rectangle.frame - self.frame) > 20:
            return False

        distance = self.are_rectangles_same(rectangle)
        if distance is False:
            return False

        if not Rectangle.are_colors_similar(self.color, rectangle.color):
            return False

        self.x, self.y, self.height, self.width, self.frame = (
            rectangle.x,
            rectangle.y,
            rectangle.width,
            rectangle.height,
            rectangle.frame,
        )
        self.data.append(
            {
                "x": rectangle.x,
                "y": (video_height - rectangle.y),
                "width": rectangle.width,
                "height": rectangle.height,
                "frame": rectangle.frame,
                "distance": distance,
                "color": self.color,
            }
        )
        return True

    def save_rectangle(self, name: int = 0):
        """Saves the rectangle's data as a JSON file.

        Args:
            name (int, optional): The name (or index) for the saved file. Defaults to 0.
        """
        filename = f"rectangle_data_{name}.json"

        rectangle_data = {
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "data": self.data,  # List of positions (dictionaries)
        }

        try:
            os.makedirs("data", exist_ok=True)
            data_file = os.path.join("data", filename)
            with open(data_file, "w", encoding="utf-8") as file:
                json.dump(rectangle_data, file, indent=4)
            logger.info("Saved data for rectangle in: %s", filename)
        except Exception as e:
            logger.error("Failed to save rectangle data: %s", e)


# Example usage of the Rectangle class
if __name__ == "__main__":
    # Initialize a rectangle
    rect1 = Rectangle(
        x=10, y=20, width=100, height=50, color=[255, 0, 0], frame=1, video_height=1080
    )
    rect2 = Rectangle(
        x=15, y=25, width=100, height=50, color=[255, 0, 0], frame=2, video_height=1080
    )

    # Check if rect2 is the same as rect1
    same = rect1.same_rectangle(rect2, video_height=1080)
    print(f"Rectangles are the same: {same}")

    # Save rectangle data to a file
    rect1.save_rectangle(name=1)
