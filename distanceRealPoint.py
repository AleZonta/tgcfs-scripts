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
            for el in json_file:
                if "size" not in el:
                    trajectories_label.append(el)

            return trajectories_label, json_file


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
    #distance in metres
    return distance * 1000

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Das5/0/"
    files = 0
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
            files+=1

    max = files
    vect = np.arange(1, max +1)
    real_distances = []
    arrays = []
    for numb in vect:
        logging.debug("Analysing trajectory " + str(numb))
        name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

        trajectories_label, json_file = reanInfo(path + name)

        # lets try the first one
        # print "----------------- first one -----------------"
        # print json_file[trajectories_label[0]]["real"]
        # print json_file[trajectories_label[0]]["generated"]
        # print json_file[trajectories_label[0]]["trajectory"]
        # # lets try the second one
        # print "----------------- second one -----------------"
        # print json_file[trajectories_label[1]]["real"]
        # print json_file[trajectories_label[1]]["generated"]
        # print json_file[trajectories_label[1]]["trajectory"]
        # # lets try the third one
        # print "----------------- third one -----------------"
        # print json_file[trajectories_label[2]]["real"]
        # print json_file[trajectories_label[2]]["generated"]
        # print json_file[trajectories_label[2]]["trajectory"]
        #
        # # transform trajectory in lat and lng
        # lat = []
        # lng = []
        # for el in json_file[trajectories_label[0]]["trajectory"]:
        #     lat.append(el[0])
        #     lng.append(el[1])

        # real points
        lat_real = []
        lng_real = []
        for el in json_file[trajectories_label[0]]["real"]:
            lat_real.append(el[0])
            lng_real.append(el[1])

        # generated points
        lat_generated = []
        lng_generated = []
        for label in trajectories_label:
            for el in json_file[label]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])

        distances = []
        # compute distance
        for i in range(len(lat_generated)):
            distances.append(float(coputeDistance(lat_real[0],lng_real[0], lat_generated[i], lng_generated[i])))


        array = np.array(distances)
        arrays.append(array)
        real_distances.append((np.max(array), np.min(array), np.median(array), np.std(array)))


    x = []
    max_value = []
    min = []
    median = []
    std = []
    x = np.arange(0, len(real_distances))
    for el in real_distances:
        max_value.append(el[0])
        min.append(el[1])
        median.append(el[2])
        std.append(el[3])

    plt.figure(0)
    sns.set_style("darkgrid")
    # plt.plot(max_value)
    # plt.plot(min)
    # plt.plot(median)
    plt.errorbar(x, median, std, linestyle='None')
    # plt.xlabel("Generation")
    # plt.ylabel("Distance (metres) point generated with real point")
    # plt.legend(("Max Distance", "Min Distance", "Median Distance"))

    plt.show()

    # os.system("rm movie.mp4")
    # os.system("ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4")
    # os.system("rm _tmp*.png")
    # logging.debug("End Program")
