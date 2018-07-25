"""
This program reads all .csv files in the current directory, and plot the AVERAGE speed
of ALL flies versus time. NO NEED to specify the file name. Plots are saved in the same
directory.

Assume csv files have the format generated by FicTrac, so USE_COL indicates the
speed column. The average speed per second is calculated, FPS indicates the
number of frames per second.

Tianxing Jiang
Jul 2, 2018
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

file_list = next(os.walk("."))[2]
FPS = 30
USE_COL = 16

table = []
min_length = 0

for file_name in file_list:
    if file_name[-3:] == "csv":
        df1 = pd.read_csv(file_name, header=None)
        ds = df1.values
        result = np.array([])
        for i in range(df1.shape[0]):
            if i % 30 == FPS-1:
                count = 0
                for j in range(i-FPS+1, i):
                    count += ds[j+1][USE_COL]-ds[j][USE_COL]
                result = np.append(result, count/FPS)
        if (min_length == 0) or (len(result) < min_length):
            min_length = len(result)
        table.append(result)
        # fig1, ax = plt.subplots()
        # ax.plot(result)
        # ax.set(xlabel='Time (s)', ylabel='Speed (rad/s)',
        #        title='Speed of fruit fly')
        # fig1.savefig(file_name[:-4]+"_speed-time.png")
        # plt.show()
table_1 = np.array([table[0][:min_length]])
print(table_1.shape)
for arr in table[1:]:
    arr = arr[:min_length]
    print(arr.shape)
    table_1 = np.vstack((table_1, arr))
table_1 = table_1.transpose()
std = np.std(table_1, axis=1)

result = np.array([])
for col in table_1:
    result = np.append(result, np.average(col))

fig1, ax = plt.subplots()
ax.plot(result)
ax.set(xlabel='Time (s)', ylabel='Turning (rad/s)',
       title='Average turning of fruit flies')

ax.fill_between(np.arange(0, len(std), 1), result+std, result-std, alpha=0.2)  # Shade the std

# ax.fill([60, 120, 120, 60], [0, 0, 3, 3], 'b', alpha=0.2)  # Shade the second minute
# ax.set_xlim(0, 180)
# ax.set_ylim(0, 3)

fig1.savefig("turning-time.png")
plt.show()

