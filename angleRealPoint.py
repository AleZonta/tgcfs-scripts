import logging
import json
import zipfile
from pandas import np
import pandas as pd
import os
from math import sin, cos, sqrt, atan2, radians, degrees, fabs
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm
import re

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


def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-plusplus10/0/"

    names = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
            names.append(i)

    names = sorted_nicely(names)

    total_distances = []
    logging.debug("Analysing Trajectories...")
    for i in tqdm.tqdm(range(len(names))):
        name = names[i]

        trajectories_label, json_file = reanInfo(path + name)

        # real points
        lat_real = []
        lng_real = []
        # generated points
        lat_generated = []
        lng_generated = []

        label_real = []
        label_generated = []
        label_trajectory = []

        # last point trajectory
        lat_last = []
        lng_last = []
        for labels in trajectories_label:
            for el in json_file[labels]["real"]:
                if el[0] not in lat_real:
                    lat_real.append(el[0])
                    lng_real.append(el[1])
                    label_real.append(json_file[labels]["id"])

            for el in json_file[labels]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])
                label_generated.append(json_file[labels]["id"])


            appo_lat = []
            appo_lgn = []
            for el in json_file[labels]["trajectory"]:
                appo_lat.append(el[0])
                appo_lgn.append(el[1])

            lat_last.append(appo_lat[len(appo_lat) - 1])
            lng_last.append(appo_lgn[len(appo_lgn) - 1])
            label_trajectory.append(json_file[labels]["id"])

        distance_per_trajectories = {}

        # for the trajectories I have
        for i in range(len(label_real)):

            # compute real bearing for the current trajectory
            real_bearing = computeBearing(lat_last[i], lng_last[i], lat_real[i], lng_real[i])

            # find index of the point generated corresponding to this trajectory
            index = [j for j, x in enumerate(label_generated) if x == label_real[i]]

            index_last_point = [j for j, x in enumerate(label_trajectory) if x == label_real[i]]

            distances = []
            for ind in index:
                bearing = computeBearing(lat_last[index_last_point[0]], lng_last[index_last_point[0]], lat_generated[ind],
                                         lng_generated[ind])
                distances.append(fabs(bearing - real_bearing))
            array = np.array(distances)

            distance_per_trajectories.update({i: (np.max(array), np.min(array), np.mean(array), np.std(array))})
        total_distances.append(distance_per_trajectories)
            # # real points
        # lat_real = []
        # lng_real = []
        # for el in json_file[trajectories_label[0]]["real"]:
        #     lat_real.append(el[0])
        #     lng_real.append(el[1])
        #
        # # generated points
        # lat_generated = []
        # lng_generated = []
        # for label in trajectories_label:
        #     for el in json_file[label]["generated"]:
        #         lat_generated.append(el[0])
        #         lng_generated.append(el[1])

        # last point trajectory
        # lat_last = []
        # lng_last = []
        # for el in json_file[trajectories_label[0]]["trajectory"]:
        #     lat_last.append(el[0])
        #     lng_last.append(el[1])

        # real_bearing = computeBearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_real[0], lng_real[0])
        #
        # distances = []
        # # compute distance
        # for i in range(len(lat_generated)):
        #     # compute the distances
        #     bearing = computeBearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_generated[i], lng_generated[i])
        #     distances.append(fabs(bearing - real_bearing))
        #
        # array = np.array(distances)
        # real_distances.append((np.max(array), np.min(array), np.mean(array), np.std(array)))

    x = []
    x = np.arange(0, len(total_distances))
    max_value = []
    min = []
    mean = []
    std = []
    for el in total_distances:
        a = []
        b = []
        c = []
        d = []
        for k in el.keys():
            a.append(el[k][0])
            b.append(el[k][1])
            c.append(el[k][2])
            d.append(el[k][3])
        max_value.append(np.mean(np.array(a)))
        min.append(np.mean(np.array(b)))
        mean.append(np.mean(np.array(c)))
        std.append(np.mean(np.array(d)))


    plt.figure(0)
    sns.set_style("darkgrid")
    plt.errorbar(x, mean, std)
    plt.errorbar(x, min)
    plt.errorbar(x, max_value)
    # plt.xlabel("Generation")
    # plt.ylabel("Difference in bearing points")
    plt.legend(("mean Difference", "min Difference", "max Difference"))

    plt.show()


