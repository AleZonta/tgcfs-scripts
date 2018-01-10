import logging
import json
import zipfile
from pandas import np
import pandas as pd
import os
from math import sin, cos, sqrt, atan2, radians, degrees, fabs
import matplotlib.pyplot as plt
import seaborn as sns

from fitnessAngleDistance import how_many_folder, analise_distances


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Volumes/TheMaze/TuringLearning/Experiment Christmas Holidays/Experiment-commalambda100"
    folders = how_many_folder(path)
    num_folder = len(folders)
    logging.debug("Folder to analise -> " + str(num_folder))

    all_real_distances = []
    all_bearing_distances = []
    for folder in folders:
        logging.debug("Analysing folder " + str(folder))

        real_path = path + "/" + str(folder) + "/"

        files = 0
        for i in os.listdir(real_path):
            if os.path.isfile(os.path.join(real_path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                files += 1

        vect = np.arange(1, files + 1)

        # read all the trajectories for the distance to the real point
        logging.debug("Checking the distances")
        real_distances, real_distances_bearing = analise_distances(path, folder)

        x = []
        median = []
        std = []
        x = np.arange(0, len(real_distances))
        for el in real_distances:
            median.append(el[2])
            std.append(el[3])

        all_real_distances.append((x, median, std))

        x_bearing = []
        median_bearing = []
        std_bearing = []
        x_bearing = np.arange(0, len(real_distances_bearing))
        for el in real_distances_bearing:
            median_bearing.append(el[2])
            std_bearing.append(el[3])

        all_bearing_distances.append((x_bearing, median_bearing, std_bearing))

    logging.debug("Computing the graph")

    plt.figure(figsize=(16, 8))
    sns.set_style("darkgrid")
    for el in all_real_distances:
        plt.errorbar(el[0], el[1], el[2], elinewidth=0.5)
    plt.xlabel("Generation")
    plt.ylabel("Distance points generated to real point")
    plt.legend(folders)

    plt.figure(figsize=(16, 8))
    sns.set_style("darkgrid")
    for el in all_bearing_distances:
        plt.errorbar(el[0], el[1], el[2], elinewidth=0.5)
    plt.xlabel("Generation")
    plt.ylabel("Difference bearing real point from generated points")
    plt.legend(folders)

    plt.show()