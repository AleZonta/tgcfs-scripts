from __future__ import print_function
import logging

import gmplot
import json
import zipfile
from pandas import np
import pandas as pd
import imgkit
from selenium import webdriver
import time
import os
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
import seaborn as sns


def reanInfo(path):
    # logging.debug("reading ZIP file")
    with zipfile.ZipFile(path) as z:
        with z.open(z.namelist()[0]) as f:
            content = f.readlines()
            content = content[0].replace("(", "[").replace(")", "]")
            pos = content.find("{")
            content = content[pos:]
            json_file = json.loads(content)

            trajectories_label = []

            id_label = []

            for el in json_file:
                if "size" not in el:
                    trajectories_label.append(el)
                    idd = json_file[el]["id"]
                    if idd not in id_label:
                        id_label.append(idd)

            return trajectories_label, json_file, id_label


def coputeDistance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    # distance in metres
    return distance * 1000


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-testnewTrajcetroies/2/"
    files = 0
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
            files += 1

    max = files
    vect = np.arange(1, max + 1)
    total_distances = []
    for numb in vect:
        logging.debug("Analysing trajectory " + str(numb))
        name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

        trajectories_label, json_file, id_label = reanInfo(path + name)

        # number = 0
        # while number < len(id_label):

        # real points
        lat_real = []
        lng_real = []
        # generated points
        lat_generated = []
        lng_generated = []

        label_real = []
        label_generated = []
        for labels in trajectories_label:
            for el in json_file[labels]["real"]:
                if el[0] not in lat_real:
                    lat_real.append(el[0])
                    lng_real.append(el[1])
                    label_real.append(json_file[labels]["id"])

            for el in json_file[labels]["generated"]:
                if el[0] not in lat_generated:
                    lat_generated.append(el[0])
                    lng_generated.append(el[1])
                    label_generated.append(json_file[labels]["id"])


        distances = []
        # now for every trajectory compute the distance of the generated distance
        for i in range(len(label_real)):
            index = [j for j, x in enumerate(label_generated) if x == label_real[i]]
            for ind in index:
                distances.append(
                    float(coputeDistance(lat_real[i], lng_real[i], lat_generated[ind], lng_generated[ind])))

        array = np.array(distances)
        total_distances.append((np.max(array), np.min(array), np.mean(array), np.std(array)))
        # total_distances.append(distance_per_trajectories)

    x = []
    x = np.arange(0, len(total_distances))
    max_value = []
    min = []
    mean = []
    std = []
    for el in total_distances:
        # a = []
        # b = []
        # c = []
        # d = []
        # for k in el.keys():
        #     a.append(el[k][0])
        #     b.append(el[k][1])
        #     c.append(el[k][2])
        #     d.append(el[k][3])
        max_value.append(el[0])
        min.append(el[1])
        mean.append(el[2])
        std.append(el[3])

    plt.figure(0)
    sns.set_style("darkgrid")
    plt.errorbar(x, mean, std)
    plt.errorbar(x, min)
    plt.errorbar(x, max_value)
    # plt.plot(median)
    plt.legend(("mean Difference", "min Difference", "max Difference"))
    # plt.xlabel("Generation")
    # plt.ylabel("Distance (metres) point generated with real point")
    # plt.legend(("Max Distance", "Min Distance", "Median Distance"))

    plt.show()

    # os.system("rm movie.mp4")
    # os.system("ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4")
    # os.system("rm _tmp*.png")
    # logging.debug("End Program")
