"""
This program reads all .csv files in the current directory, and plot the speed
versus time. NO NEED to specify the file name. Plots are saved in the same
directory.

Assume csv files have the format generated by FicTrac, so USE_COL indicates the
speed column. The average speed per second is calculated, FPS indicates the
number of frames per second.

Tianxing Jiang
Apr 13, 2018
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

file_list = next(os.walk("."))[2]
FPS = 30
USE_COL = 18

for file_name in file_list:
    if file_name[-3:] == "csv":
        df1 = pd.read_csv(file_name, header=None)
        ds = df1.values
        result = np.ndarray([0])
        for i in range(df1.shape[0]):
            if i % 30 == FPS-1:
                count = 0
                for j in range(i-FPS+1, i):
                    count += ds[j][USE_COL]
                result = np.append(result, count)

        fig1, ax = plt.subplots()
        ax.plot(result)
        ax.set(xlabel='Time (s)', ylabel='Speed (rad/s)',
               title='Speed of fruit fly')
        fig1.savefig(file_name[:-3]+"_speed-time.png")
        plt.show()
