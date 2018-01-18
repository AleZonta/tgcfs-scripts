import logging
import json
import zipfile
from pandas import np
import pandas as pd
import os
from math import sin, cos, sqrt, atan2, radians, degrees, fabs
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


def computeBearing(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    bearing = atan2(sin(lon2 - lon1) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    return bearing


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-testnewoutput/1/"
    files = 0
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
            files += 1

    max = files
    vect = np.arange(1, max +1)
    real_distances = []
    for numb in vect:
        if numb%100 == 0:
            logging.debug("Analysing trajectory " + str(numb))
        name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

        trajectories_label, json_file = reanInfo(path + name)


        if numb == 810:
            test_stop_here = True

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

        # last point trajectory
        lat_last = []
        lng_last = []
        for el in json_file[trajectories_label[0]]["trajectory"]:
            lat_last.append(el[0])
            lng_last.append(el[1])

        real_bearing = computeBearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_real[0], lng_real[0])

        distances = []
        # compute distance
        for i in range(len(lat_generated)):
            # compute the distances
            bearing = computeBearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_generated[i], lng_generated[i])
            distances.append(fabs(bearing - real_bearing))

        array = np.array(distances)
        real_distances.append((np.max(array), np.min(array), np.mean(array), np.std(array)))


    max_value = []
    min = []
    mean = []
    std = []
    x = np.arange(0, len(real_distances))
    for el in real_distances:
        max_value.append(el[0])
        min.append(el[1])
        mean.append(el[2])
        std.append(el[3])


    plt.figure(0)
    sns.set_style("darkgrid")
    plt.errorbar(x, mean, std)
    plt.errorbar(x, min)
    plt.errorbar(x, max_value)
    # plt.xlabel("Generation")
    # plt.ylabel("Difference in bearing points")
    plt.legend(("mean Difference", "min Difference", "max Difference"))

    plt.show()


