from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import pandas as pd
import numpy as np

import tkinter as tk

INDEX_DICT = {
    "frame": 0,
    "delta_rotation_cam_x": 1,
    "delta_rotation_cam_y": 2,
    "delta_rotation_cam_z": 3,
    "delta_rotation_score": 4,
    "delta_rotation_lab_x": 5,
    "delta_rotation_lab_y": 6,
    "delta_rotation_lab_z": 7,
    "abs_orientation_cam_x": 8,
    "abs_orientation_cam_y": 9,
    "abs_orientation_cam_z": 10,
    "abs_orientation_lab_x": 11,
    "abs_orientation_lab_y": 12,
    "abs_orientation_lab_z": 13,
    "position_x": 14,
    "position_y": 15,
    "heading": 16,
    "movement": 17,
    "speed": 18,
    "side_x": 19,
    "side_y": 20,
    "timestamp": 21,
    "sequence": 22
}


class PlotHelper(object):
    """
    Class to help plot the graph, with prev and next button on the tk canvas
    """
    def __init__(self, canvas_frame, file_list):
        self.canvas_frame = canvas_frame
        self.file_list = file_list
        self.count = len(file_list)
        self.index = 0  # Currently at the first file

    def has_next(self):
        """
        Return True if there is a next file, False if at the last file
        """
        return self.index < self.count-1

    def has_prev(self):
        """
        Return True if there is a previous file, False if at the first file
        """
        return self.index > 0

    def plot_next(self, x, y, xc, yc, title):
        if not self.has_next():
            return
        self.index += 1
        self.plot(x, y, xc, yc, title)

    def plot_prev(self, x, y, xc, yc, title):
        if not self.has_prev():
            return
        self.index -= 1
        self.plot(x, y, xc, yc, title)

    def plot(self, x, y, xc, yc, title):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        X = self._read_file(self.file_list[self.index], 0)  # TODO: optimization, don't open file twice
        Y = self._read_file(self.file_list[self.index], y)
        fig = Figure(figsize=(4, 3))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.plot(X, Y)
        ax.set_xlabel(xc)
        ax.set_ylabel(yc)
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.show()

    def _read_file(self, path, col):
        """
        A helper method to read the file for the desired column
        :param path: string, the path of a single file
        :param col: int, the index of column
        :return: a numpy array
        """
        ds = pd.read_csv(path, header=None).get_values()
        result = np.array(ds[:, col])
        return result

    def save_file(self, path, extension, size):
        """
        Method to save images in the given directory

        :param path: String, The directory to save in
        :param extension: String, The file format, e.g. png, svg
        :param size: List or tuple, The size of the image, e.g. (800, 600)
        :return: None
        """
        pass
