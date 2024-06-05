"""
This script provides a Presenter class for loading, preparing, and visualizing trajectory data from JSON files.

It offers functionalities to:
    - Load JSON data from multiple files selected by the user
    - Process and prepare the data for animation
    - Create and display an animated visualization of object trajectories

The Presenter class manages the data and animation process, ensuring a smooth and informative presentation of the trajectory data.
"""

"""
This script provides a Presenter class for loading, preparing, and visualizing trajectory data from JSON files.

It offers functionalities to:
    - Load JSON data from multiple files selected by the user
    - Process and prepare the data for animation
    - Create and display an animated visualization of object trajectories

The Presenter class manages the data and animation process, ensuring a smooth and informative presentation of the trajectory data.
"""

import sys
import json
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from app.logging_config import logger


class Presenter:
    """
    This class handles loading and presenting trajectory data from JSON files.

    It provides methods to:
        - `load_json_files`: Load JSON data from multiple files.
        - `update`: Update the animation with filtered data for a specified frame.
        - `on_key_press`: Handle key press events to close the animation.
        - `present`: Load JSON files, prepare data for animation, and display the animation.

    Attributes:
        filenames (list): List of filenames corresponding to each object's data.
        min_frame (int): The minimum frame number across all data sets.
        max_frame (int): The maximum frame number across all data sets.
        max_x (float): The maximum x-coordinate value in the data.
        max_y (float): The maximum y-coordinate value in the data.
        x_coords_list (list): List of lists containing x-coordinates for each object.
        y_coords_list (list): List of lists containing y-coordinates for each object.
        frames_list (list): List of lists containing frame numbers for each object.
    """

    def __init__(self):
        """Initializes the Presenter object and its attributes.."""
        logger.info("Start of presentation")
        self.filenames = []
        self.x_coords_list = []
        self.y_coords_list = []
        self.frames_list = []
        self.min_frame = 0
        self.max_frame = 0
        self.max_x = 0
        self.max_y = 0

    def load_json_files(self):
        """
        Loads data from multiple JSON files.

        This function prompts the user to select JSON files using a graphical file dialog.
        It then attempts to load the data from each selected file, performing the following:

        - Checks if the file exists.
        - Validates the file format as JSON using `json.load`.
        - Handles potential errors gracefully using `try-except` blocks.
        - Logs success and error messages using a logger (if available).

        Returns:
            - A list of all loaded data objects (one per file).
            - A list of corresponding filenames for the loaded data.

        If no files are selected or errors occur during loading, returns None.
        """
        all_data = []
        file_names = []

        root = Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title="Select JSON data file(s) from tracker.py - circle_data_[number].py or rectangle_data_[number].py ",
            filetypes=[("JSON files", "*.json")],
        )

        if not file_paths:
            logger.error("No files selected.")
            return None, None

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_data = json.load(file)["data"]
                    file_names.append(file_path.split("/")[-1])
                    all_data.append(file_data)
                    logger.info("File '%s' successfully loaded.", file_path)
            except FileNotFoundError:
                logger.error("File '%s' not found.", file_path)
                continue
            except json.JSONDecodeError:
                logger.error("File '%s' is not a valid JSON file.", file_path)
                continue
            except Exception as e:
                logger.error("Error loading file '%s': %s", file_path, e)
                continue

        return all_data, file_names

    def update(self, frame):
        """
        Updates the animation with the filtered data for the specified frame.

        This function iterates through multiple datasets (assumed to be stored in
        self.x_coords_list, self.y_coords_list, and self.filenames) and updates the plot
        with filtered data points up to the given frame number.

        This function clears the current plot and re-draws the trajectories of objects up to the specified frame. It updates the plot with the following settings:
        - Draws trajectories for each object using the x and y coordinates.
        - Only includes points where coordinates are not equal to -1.
        - Labels each trajectory with the filename it came from.
        - Sets the aspect ratio to be equal for both axes.
        - Sets the x and y axis limits to predefined maximum values.
        - Adds grid lines to both axes with a specified style and interval.
        - Adds a legend to the plot.

        Args:
            frame (int): : The current frame number in the animation.

        Attributes used:
        - self.x_coords_list (list): List of x-coordinates for each object.
        - self.y_coords_list (list): List of y-coordinates for each object.
        - self.filenames (list): List of filenames corresponding to each object.
        - self.min_frame (int): The minimum frame number to display.
        - self.max_x (float): The maximum value for the x-axis.
        - self.max_y (float): The maximum value for the y-axis

        Returns:
            None
        """
        plt.cla()
        for x_coords, y_coords, filename in zip(
            self.x_coords_list, self.y_coords_list, self.filenames
        ):
            filtered_points = [
                (x, y)
                for x, y in zip(x_coords[: frame + 1], y_coords[: frame + 1])
                if x != -1 and y != -1
            ]

            if filtered_points:
                filtered_x, filtered_y = zip(*filtered_points)
                plt.plot(
                    filtered_x,
                    filtered_y,
                    marker="o",
                    label=filename,
                )
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.title(f"Object Path (Frame {frame+self.min_frame-1}) On Enter close.")
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlim(0, max(500, self.max_x))
        plt.ylim(0, max(500, self.max_y))
        plt.legend()
        plt.grid(
            True,
            which="both",
            linestyle="--",
            linewidth=0.5,
            color="gray",
            axis="x",
            alpha=0.7,
            markevery=20,
        )
        plt.grid(
            True,
            which="both",
            linestyle="--",
            linewidth=0.5,
            color="gray",
            axis="y",
            alpha=0.7,
            markevery=20,
        )

    def on_key_press(self, event):
        """Handles key press events to close the animation on Enter key."""
        if event.key == "enter":
            logger.info("End of presentation")
            plt.close(event.canvas.figure)
            sys.exit(0)

    def present(self):
        """
        Loads data from JSON files, prepares the data for animation, and displays the animation.

        This function performs the following steps:

        1. Loads data from JSON files using the `load_json_files` method (assumed to be implemented elsewhere).
        2. Checks if data was loaded successfully.
        3. If data exists:
            - Initializes empty lists for x-coordinates, y-coordinates, and frame numbers.
            - Iterates through each data set in the loaded data.
                - Extracts x-coordinates, y-coordinates, and frame numbers from each data point.
                - Appends the extracted data to their respective lists.
            - Finds the minimum and maximum frame numbers across all data sets.
            - Finds the maximum x and y values across all data sets for setting axis limits.
            - Creates a new list with dictionaries for each data set.
                - Each dictionary has keys representing frame numbers and values as (-1, -1) initially.
                - The function then iterates through each data point again, updating the corresponding frame number key in the dictionary with the actual x and y values.
            - Re-initializes empty lists for x-coordinates, y-coordinates, and frames.
            - Iterates through the list of dictionaries (prepared data).
                - Extracts non-empty x-coordinates, y-coordinates, and frame numbers from each dictionary.
                - Appends the extracted data to their respective lists.
        4. Creates a Matplotlib figure with a size based on the maximum x and y values.
        5. Creates an animation using `animation.FuncAnimation`.
            - The animation calls the `update` function for each frame.
            - The number of frames is set to the maximum length of any data set.
            - An interval of 10 milliseconds is set between frames (can be adjusted for speed).
        6. Enables a grid on the plot using `plt.grid(True)`.
        7. Displays the animation using `plt.show()`.

        Attributes used:
        - self.filenames (list): List of filenames corresponding to each object.
        - self.min_frame (int): The minimum frame number in the dataset.
        - self.max_frame (int): The maximum frame number in the dataset.
        - self.max_x (float): The maximum x-coordinate value in the dataset.
        - self.max_y (float): The maximum y-coordinate value in the dataset.
        - self.x_coords_list (list): List of lists containing x-coordinates for each object.
        - self.y_coords_list (list): List of lists containing y-coordinates for each object.
        - self.frames_list (list): List of lists containing frame numbers for each object.

        Methods called:
        - self.load_json_files(): Loads JSON files and returns the data along with filenames.
        - self.update(frame): Updates the plot for the given animation frame.

        The animation is displayed using matplotlib's FuncAnimation and is shown in a window.
        """
        data_list, self.filenames = self.load_json_files()

        if data_list:
            x_coords_list = []
            y_coords_list = []
            frames_list = []

            for data in data_list:
                x_coords = [point["x"] for point in data]
                y_coords = [point["y"] for point in data]
                frames = [point["frame"] for point in data]
                x_coords_list.append(x_coords)
                y_coords_list.append(y_coords)
                frames_list.append(frames)

            flat_list = [item for sublist in frames_list for item in sublist]
            self.min_frame = min(flat_list)
            self.max_frame = max(flat_list)
            flat_list = [item for sublist in x_coords_list for item in sublist]
            self.max_x = max(flat_list)
            flat_list = [item for sublist in y_coords_list for item in sublist]
            self.max_y = max(flat_list)

            full_data_list = []
            for data in data_list:
                new_dict = {i: (-1, -1) for i in range(self.min_frame, self.max_frame)}
                for point in data:
                    new_dict[point["frame"]] = (point["x"], point["y"])
                full_data_list.append(new_dict)

            for data in full_data_list:
                x_coords = [data[x][0] for x in data if data[x] is not None]
                y_coords = [data[x][1] for x in data if data[x] is not None]
                frames = [x for x in data]

                self.x_coords_list.append(x_coords)
                self.y_coords_list.append(y_coords)
                self.frames_list.append(frames)

            fig = plt.figure(
                figsize=(max(8, self.max_y / 100), max(6, self.max_x / 100))
            )

            ani = animation.FuncAnimation(
                fig, self.update, frames=max(map(len, self.frames_list)), interval=10
            )

            # Connect the key press event to the on_key_press function
            fig.canvas.mpl_connect("key_press_event", self.on_key_press)

            plt.grid(True)
            plt.show()


if __name__ == "__main__":
    presenter = Presenter()
    presenter.present()
