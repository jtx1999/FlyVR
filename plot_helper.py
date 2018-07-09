from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import os
import tkinter as tk

INDEX_SHORT_DICT = {
    "Speed": 18,
    "Turning": 16
}

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

INDIVIDUAL_PLOT = 1
AVERAGE_PLOT = 2
FPS = 30


class PlotHelper(object):
    """
    Class to help plot the graph, with prev and next button on the tk canvas
    """
    def __init__(self, canvas_frame, file_list, average_type=INDIVIDUAL_PLOT):
        self.canvas_frame = canvas_frame
        self.file_list = file_list
        self.index = 0
        self.set_average_type(average_type)

    def set_average_type(self, average_type=INDIVIDUAL_PLOT):
        self.average_type = average_type
        if average_type == INDIVIDUAL_PLOT:
            self.count = len(self.file_list)
        elif average_type == AVERAGE_PLOT:
            self.count = 1
            self.index = 0

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
        fig = Figure(figsize=(4, 3))
        ax = fig.add_axes([0.12, 0.15, 0.8, 0.75])
        ax.set_xlabel(xc)
        ax.set_ylabel(yc)
        ax.set_title(title)

        if self.average_type == INDIVIDUAL_PLOT:
            cols = self._read_file(self.file_list[self.index], x, y)
            X = cols[0]
            Y = cols[1]
            result = self._average_helper(Y, y)
            ax.plot(np.arange(len(result)), result)
        elif self.average_type == AVERAGE_PLOT:
            table = []
            min_length = 0

            for filename in self.file_list:
                cols = self._read_file(filename, x, y)
                Y = cols[1]
                result = self._average_helper(Y, y)
                if (min_length == 0) or (len(result) < min_length):
                    min_length = len(result)
                table.append(result)

            table_1 = np.array([table[0][:min_length]])
            for arr in table[1:]:
                arr = arr[:min_length]
                table_1 = np.vstack((table_1, arr))
            table_1 = table_1.transpose()
            std = np.std(table_1, axis=1)
            result = np.array([])
            for col in table_1:
                result = np.append(result, np.average(col))
            ax.plot(np.arange(len(result)), result)

            ax.fill_between(np.arange(0, len(std), 1), result + std, result - std, alpha=0.2)  # Shade the std
            if y == 18:
                ax.fill([60, 120, 120, 60], [0, 0, 3, 3], 'b', alpha=0.2)  # Shade the second minute
                ax.set_xlim(0, 180)
                ax.set_ylim(0, 3)
            elif y == 16:  # The plot for turning
                ax.fill([60, 120, 120, 60], [-0.3, -0.3, 0.3, 0.3], 'b', alpha=0.2)
                ax.set_xlim(0, 180)
                ax.set_ylim(-0.3, 0.3)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.show()
        print("Done plotting")

    def _read_file(self, path, col1, col2):
        """
        A helper method to read the file for the desired column
        :param path: string, the path of a single file
        :param col1: int, the index of column
        :param col2: int, the index of the second column
        :return: a numpy array
        """
        ds = pd.read_csv(path, header=None).get_values()
        result1 = np.array(ds[:, col1])
        result2 = np.array(ds[:, col2])
        return np.array([result1, result2])

    def save_file(self, path, extension, size, x, y, xc, yc, title):
        """
        Method to save images in the given directory

        :param path: String, The directory to save in
        :param extension: String, The file format, e.g. png, svg
        :param size: List or tuple, The size of the image, e.g. (800, 600)
        :return: None
        """

        if self.average_type == INDIVIDUAL_PLOT:
            for file_path in self.file_list:
                fig = plt.figure()
                ax = plt.subplot(111)
                ax.set_xlabel(xc)
                ax.set_ylabel(yc)
                ax.set_title(title)
                result = np.ndarray([0])
                cols = self._read_file(self.file_list[self.index], x, y)
                X = cols[0]
                Y = cols[1]
                result = self._average_helper(Y, y)
                ax.plot(np.arange(len(result)), result)
                file_name = os.path.split(file_path)[-1]
                file_name, _ = os.path.splitext(file_name)
                fig.savefig(path + "/" + file_name + "-" + title + "." + extension, figsize=size)
        elif self.average_type == AVERAGE_PLOT:
            table = []
            min_length = 0
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.set_xlabel(xc)
            ax.set_ylabel(yc)
            ax.set_title(title)
            for filename in self.file_list:
                cols = self._read_file(filename, x, y)
                Y = cols[1]
                result = self._average_helper(Y, y)
                if (min_length == 0) or (len(result) < min_length):
                    min_length = len(result)
                table.append(result)

            table_1 = np.array([table[0][:min_length]])
            for arr in table[1:]:
                arr = arr[:min_length]
                table_1 = np.vstack((table_1, arr))
            table_1 = table_1.transpose()
            std = np.std(table_1, axis=1)
            result = np.array([])
            for col in table_1:
                result = np.append(result, np.average(col))
            ax.plot(np.arange(len(result)), result)

            ax.fill_between(np.arange(0, len(std), 1), result + std, result - std, alpha=0.2)  # Shade the std
            if y == 18:  # The plot for speed
                ax.fill([60, 120, 120, 60], [0, 0, 3, 3], 'b', alpha=0.2)  # Shade the second minute
                ax.set_xlim(0, 180)
                ax.set_ylim(0, 3)
            elif y == 16:  # The plot for turning
                ax.fill([60, 120, 120, 60], [-0.3, -0.3, 0.3, 0.3], 'b', alpha=0.2)
                ax.set_xlim(0, 180)
                ax.set_ylim(-0.3, 0.3)
            fig.savefig(path + "/" + "Average Plot" + "-" + title + "." + extension, figsize=size)

    def get_index(self):
        """
        Return the current index
        """
        return self.index

    def get_file_name(self, index):
        """
        Return a string of the file name at the index
        File name only, no extension or path
        """
        result = os.path.split(self.file_list[index])[-1]
        filename, extension = os.path.splitext(result)
        return filename

    def _average_helper(self, Y, y):
        """
        :param Y: The read col
        :param y: the col number
        :return: A numpy array of averaged col
        """
        result = np.ndarray([0])
        for i in range(len(Y)):
            if i % 30 == FPS - 1:
                count = 0
                for j in range(i - FPS + 1, i):
                    if y == 16:  # Turning
                        count += (Y[j + 1] - Y[j])
                    else:
                        count += Y[j]
                if y == 16:  # Turning
                    result = np.append(result, count / FPS)
                else:
                    result = np.append(result, count)
        return result
