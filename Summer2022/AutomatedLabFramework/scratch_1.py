import os
import csv

import matplotlib.pyplot as plt

fl = list(os.walk("./temp/data/repeat runs"))

files_of_concern = []

for data in fl[1:]:
    path, sub_folders, file_names = data

    with open(f"{path}/SUMMARY.csv", 'r') as summary_file:

        lines = summary_file.readlines()

        theta_list = [float(((line.split(","))[0]).strip()) for line in lines[1:]]
        c4_list = [float(((line.split(","))[10]).strip()) for line in lines[1:]]

        plt.plot(theta_list, c4_list)
        plt.show()

        decreasing = True
        for i in range(len(c4_list)):
            try:
                if c4_list[i+1] > c4_list[i]:
                    decreasing = False
                    break
            except:
                break

        if not decreasing:
            files_of_concern.append(path)