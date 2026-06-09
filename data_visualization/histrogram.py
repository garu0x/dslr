import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helper_functions.min import ft_min
from helper_functions.max import ft_max
from helper_functions.avg import ft_avg
from helper_functions.percentile import ft_percentile
from helper_functions.std import ft_std

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

if len(sys.argv) != 2:
    print("You need a single file path")
    exit(1)
with open(sys.argv[1]) as file:
    csv_reader = csv.DictReader(file, delimiter=",")
    columns = csv_reader.fieldnames

# 1st function: get all house names and subjects
    hogwarts_house = []
    subjects = []
    count = 1
    for row in csv_reader:
        if count:
            for index in row:
                if index not in subjects and index != "Index":
                    try:
                        float(row[index])
                        subjects.append(index)
                    except ValueError:
                        pass
                count = 0
        if row["Hogwarts House"] not in hogwarts_house:
            hogwarts_house.append(row["Hogwarts House"])

    file.seek(0)
    csv_reader = csv.DictReader(file, delimiter=",")
# 2nd function: create datasets for each house
    db_houses = {house: [] for house in hogwarts_house}
    for row in csv_reader:
        if row["Hogwarts House"] in hogwarts_house:
            db_houses[row["Hogwarts House"]].append(row)

# 3rd function plot them for each subject

fig, axs = plt.subplots(3, 5, figsize=(22, 12))

for ax in axs.flat:
    ax.set(xlabel='Score', ylabel='Number of Students')
    ax.tick_params(labelsize=7)

colors = ['royalblue', 'forestgreen', 'firebrick', 'goldenrod']
colors_n = 0
for houses in hogwarts_house:
    print(f"==={houses}===")
    tmp = {classes: [] for classes in subjects}
    count_x = 0
    count_y = 0
    min_std = float('inf')
    min_subject = None  
    for classes in subjects:
        if count_y == 5:
            count_y = 0
            count_x += 1
        for rows in db_houses[houses]:
            try:
                tmp[classes].append(float(rows[classes]))
            except ValueError:
                continue
        std_val = ft_std(tmp[classes])
        if std_val < min_std:
            min_std = std_val
            min_subject = classes
        axs[count_x, count_y].hist(tmp[classes], histtype='step', bins=30, color=colors[colors_n], label=houses)
        axs[count_x, count_y].set_title(classes)
        count_y+=1
    colors_n +=1
    # plt.hist(tmp[min_subject])
    # plt.title(f"Score Distribution for '{min_subject}' by {houses}")
    print(f"Subject with lowest standard deviation for {houses}: {min_subject} ({min_std})")

for ax in axs.flat:
    if not ax.has_data():
        ax.set_visible(False)

handles = [plt.Line2D([0], [0], color=c, linewidth=2) for c in colors]
fig.legend(handles, hogwarts_house, loc='lower right', fontsize=30,title='House', title_fontsize=45, framealpha=0.8)
plt.tight_layout(pad=2.0, h_pad=3.0, w_pad=2.0)
plt.savefig('histogram_output.png')
print("Saved to histogram_output.png")
print("Done")