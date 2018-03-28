from __future__ import print_function
import logging

import gmplot
import json
import zipfile
from pandas import np
import pandas as pd
from pandas import DataFrame
import imgkit
from selenium import webdriver
import time
import os
from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm
import re
from visPointGenNoGoogle import how_many_folder, how_many_fatherFolder, find_max_fitnes, sorted_nicely


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
                if "size" not in el and "git-" not in el:
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

def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def meanAllAgents(old_path):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    folders = how_many_fatherFolder(old_path)
    dff = DataFrame(columns=['exp', 'trajectories', 'MSD'])
    iii = 0
    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        name_experiement = str(experiemnt).replace("Experiment-tgcfs-", "").replace("-ETH", "")
        second_path = old_path + experiemnt + "/"
        res = how_many_folder(second_path)
        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))



        for el in res:
            path = second_path + str(el) + "/"
            tratt = str(el)

            names = []
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)) and 'trajectory-generate-aSs-' in i and ".zip" in i:
                    names.append(i)

            names = sorted_nicely(names)

            total_distances = []
            numb = 0
            logging.debug("Analysing Trajectories...")
            for i in tqdm.tqdm(range(len(names))):
                name = names[i]
                numb += 1
                # name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

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

                distance_per_trajectories = {}
                # now for every trajectory compute the distance of the generated distance
                for i in range(len(label_real)):
                    index = [j for j, x in enumerate(label_generated) if x == label_real[i]]
                    distances = []
                    for ind in index:
                        a = np.array((lat_real[i], lng_real[i]))
                        b = np.array((lat_generated[ind], lng_generated[ind]))
                        value = np.linalg.norm(a - b) * 100000
                        value = pow(value, 2)
                        distances.append(value)

                    array = np.array(distances)
                    MSD = (np.sum(array)) / len(array)
                    distance_per_trajectories.update({i: MSD})
                total_distances.append(distance_per_trajectories)
            #
            # df = DataFrame(columns=['gen', 'tra', 'MSD'])
            #
            # x = []
            # x = np.arange(0, len(total_distances))
            # i = 0
            # for el in total_distances:
            #     for k in el.keys():
            #         d = {"gen": i, "tra": k, "MSD": el[k]}
            #         dfs = DataFrame(data=d, index=[i])
            #         df = df.append(dfs)
            #     i += 1
            # sns.set_style("darkgrid")
            # df = df[df.columns].astype(float)
            # g = sns.lmplot(x="gen", y="MSD", hue="tra", data=df, scatter_kws={"s": 1}, fit_reg=False)

            last_line = total_distances[len(total_distances) - 1]
            arr = []
            for k in last_line.keys():
                arr.append(last_line[k])

            array = np.array(arr)
            MSD = (np.sum(array)) / len(array)
            logging.debug(MSD)

            dd = {"exp": name_experiement, "trajectories": tratt, "MSD": MSD}
            dfss = DataFrame(data=dd, index=[iii])
            iii += 1
            dff = dff.append(dfss)

            # df.plot(x='gen', y='MSD')
            # sns.lmplot(x="gen", y="MSD", hue="tra", data=df)

            # a = df.loc[df['tra'] == 0]
            # ax = a.plot(x='gen', y='MSD', kind='scatter', label="0")
            # for i in range(1, 5):
            #     a = df.loc[df['tra'] == i]
            #     a.plot(x='gen', y='MSD', ax=ax, kind='scatter',label=i)


            # g.set(ylim=(0, 300))

            # for j in range(5):
            #     a = df.loc[df['tra'] == j]
            #     a.plot(x='gen', y='MSD', ylim=(0,0.00000007))


            # plt.figure(0)
            # sns.set_style("darkgrid")
            # plt.errorbar(x, mean, std)
            # plt.errorbar(x, min)
            # plt.errorbar(x, max_value)
            # # plt.plot(median)
            # plt.legend(("mean Difference", "min Difference", "max Difference"))
            # plt.xlabel("Generation")
            # plt.ylabel("Distance (metres) point generated with real point")
            # plt.legend(("Max Distance", "Min Distance", "Median Distance"))

            # save_name = path + 'msd.png'
            # plt.savefig(save_name, dpi=500, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
            #             format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
            # plt.close()
            # logging.debug("Graph saved!")

            # os.system("rm movie.mp4")
            # os.system("ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4")
            # os.system("rm _tmp*.png")
            # logging.debug("End Program")
    sns.factorplot(x="exp", y="MSD", hue="trajectories", data=dff, kind="bar",
                   palette="muted")
    plt.show()
def allTheAgents(path):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    names = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generate-aSs-' in i and ".zip" in i:
            names.append(i)

    names = sorted_nicely(names)

    total_distances = []
    numb = 0
    logging.debug("Analysing Trajectories...")
    for i in tqdm.tqdm(range(len(names))):
        name = names[i]
        numb += 1
        # name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

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

        distance_per_trajectories = {}
        # now for every trajectory compute the distance of the generated distance
        for i in range(len(label_real)):
            index = [j for j, x in enumerate(label_generated) if x == label_real[i]]
            distances = []
            for ind in index:
                a = np.array((lat_real[i], lng_real[i]))
                b = np.array((lat_generated[ind], lng_generated[ind]))
                value = np.linalg.norm(a - b) * 100000
                value = pow(value, 2)
                distances.append(value)

            array = np.array(distances)
            distance_per_trajectories.update({i: array})
        total_distances.append(distance_per_trajectories)

    df = DataFrame(columns=['gen', 'tra', "ind", 'distance'])

    x = []
    x = np.arange(0, len(total_distances))
    i = 0
    number_of_trajectories = 0
    for el in total_distances:
        number_of_trajectories = len(el.keys())
        for k in el.keys():
            array = el[k]
            q = len(array)

            for qq in range(q):
                d = {"gen": i, "tra": k, "ind": qq, "distance": array[qq]}
                dfs = DataFrame(data=d, index=[i])
                df = df.append(dfs)
        i += 1
    sns.set_style("darkgrid")
    df = df[df.columns].astype(float)



    # g = sns.lmplot(x="gen", y="MSD", hue="tra", data=df, scatter_kws={"s": 1}, fit_reg=False)
    # g.set(ylim=(0, 0.0000004))

    for tra in range(number_of_trajectories):
        a = df.loc[df['tra'] == tra]
        g = sns.lmplot(x="gen", y="distance", hue="ind", data=a, scatter_kws={"s": 1}, fit_reg=False)
        g.set(ylim=(0, 120))


    plt.show()


if __name__ == "__main__":
    path = "/Users/alessandrozonta/Desktop/lisa/"
    meanAllAgents(path)

    # allTheAgents(path)
