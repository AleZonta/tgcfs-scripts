import sys
import logging
import zipfile
import os
import json
from pandas import np
import matplotlib.pyplot as plt
import seaborn as sns
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

def analiseTra(json_file, trajectories_label):




    for trajectory in trajectories_label:

        lat = []
        lng = []
        for el in json_file[trajectory]["trajectory"]:
            lat.append(el[0])
            lng.append(el[1])

        # transform real in lat and lng

        lat_real_h = []
        lng_real_h = []

        for el in json_file[trajectory]["real"]:
            lat_real_h.append(el[0])
            lng_real_h.append(el[1])

        # transform generated in lat and lng
        lat_generated = []
        lng_generated = []
        for el in json_file[trajectory]["generated"]:
            lat_generated.append(el[0])
            lng_generated.append(el[1])

        min_lat = []
        min_lat.append(np.amin(np.array(lat)))
        min_lat.append(np.amin(np.array(lat_real_h)))
        min_lat.append(np.amin(np.array(lat_generated)))
        real_total_min_lat = np.amin(np.array(min_lat))

        min_lon = []
        min_lon.append(np.amin(np.array(lng)))
        min_lon.append(np.amin(np.array(lng_real_h)))
        min_lon.append(np.amin(np.array(lng_generated)))
        real_total_min_lng = np.amin(np.array(min_lon))

        max_lat = []
        max_lat.append(np.amax(np.array(lat)))
        max_lat.append(np.amax(np.array(lat_real_h)))
        max_lat.append(np.amax(np.array(lat_generated)))
        real_total_max_lat = np.amax(np.array(max_lat))

        max_lon = []
        max_lon.append(np.amax(np.array(lng)))
        max_lon.append(np.amax(np.array(lng_real_h)))
        max_lon.append(np.amax(np.array(lng_generated)))
        real_total_max_lng = np.amax(np.array(max_lon))

    return real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng


def manyTrajectories(json_file, trajectories_label, numb):
    total_list_different_trajectories = {}

    total_trajectories = []

    total_info_trajectories = []

    count = 0

    for trajectory in trajectories_label:

        # transform trajectory in lat and lng
        lat_real = json_file[trajectory]["trajectory"][1][0]
        lng_real = json_file[trajectory]["trajectory"][1][1]

        key = str(lat_real) + str(lng_real)

        if key not in total_list_different_trajectories:
            total_list_different_trajectories.update({key: count})
            count += 1

            lat = []
            lng = []
            for el in json_file[trajectory]["trajectory"]:
                lat.append(el[0])
                lng.append(el[1])

            # transform real in lat and lng
            lat_real_h = []
            lng_real_h = []
            for el in json_file[trajectory]["real"]:
                lat_real_h.append(el[0])
                lng_real_h.append(el[1])

            total_trajectories.append(
                {"lats_tra": lat, "lng_tra": lng, "lats_real": lat_real_h, "lng_real": lng_real_h})

            # transform generated in lat and lng
            lat_generated = []
            lng_generated = []
            for el in json_file[trajectory]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])

            vect_generated = []
            vect_generated.append((lat_generated, lng_generated))
            total_info_trajectories.append(vect_generated)
        else:
            position = total_list_different_trajectories[key]

            # transform generated in lat and lng
            lat_generated = []
            lng_generated = []
            for el in json_file[trajectory]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])

            total_info_trajectories[position].append((lat_generated, lng_generated))





    for i in range(len(total_trajectories)):
        j = i + 1
        plt.subplot(3, 4, j)
        plt.axis('off')

        lats = total_trajectories[i]["lats_tra"]
        lngs = total_trajectories[i]["lng_tra"]
        # trajectory
        plt.plot(lats, lngs, color='b', marker='o', markersize=1)

        lat_real = total_trajectories[i]["lats_real"]
        lng_real = total_trajectories[i]["lng_real"]
        # print real point
        plt.plot(lat_real, lng_real, color='k', marker='o', markersize=1)

        lat_g = []
        lng_g = []
        for el in total_info_trajectories[i]:
            lat_g.append(el[0])
            lng_g.append(el[1])

        # print generated point
        for k in range(len(lat_g)):
            plt.plot(lat_g[k], lng_g[k], color='r', marker='o', markersize=1)

    save_name = path + '_tmp%05d.png' % numb
    plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
    plt.close()


def plot_one_trajectory(trajectories_label, json_file, numb):
    # real_total_min_lat = 52.045906899999999
    # real_total_min_lng = 4.3315641388856605
    # real_total_max_lat = 52.045937623618009
    # real_total_max_lng = 4.3316090999999997
    real_total_min_lat = 52.00
    real_total_min_lng = 4.32
    real_total_max_lat = 52.1
    real_total_max_lng = 4.35

    logging.debug("Computing graph " + str(numb))

    plt.figure(numb)

    for ell in trajectories_label:
        printTrajectory(json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"],
                        real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng, plt,
                        json_file[ell]["classification"])

    save_name = path + '_tmp%05d.png' % numb
    plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
    plt.close()


def printTrajectory(real, generated, trajectory, real_total_min_lat, real_total_min_lng, real_total_max_lat,
                    real_total_max_lng, plt, fakeOrReal):
    # logging.debug("converting JSON list to list for the library")
    # transform trajectory in lat and lng
    lat = []
    lng = []
    for el in trajectory:
        lat.append(el[0])
        lng.append(el[1])

    # transform real in lat and lng
    lat_real = []
    lng_real = []
    for el in real:
        lat_real.append(el[0])
        lng_real.append(el[1])

    # transform generated in lat and lng
    lat_generated = []
    lng_generated = []
    for el in generated:
        lat_generated.append(el[0])
        lng_generated.append(el[1])

    sns.set_style("darkgrid")

    # plt.axis([real_total_min_lat, real_total_max_lat, real_total_min_lng, real_total_max_lng])

    # print trajectory
    plt.plot(lat, lng, color='b', marker='o')

    # print real point
    plt.plot(lat_real, lng_real, color='k', marker='o')

    # print generated point
    for i in range(len(lat_generated)):
        if fakeOrReal:
            plt.plot(lat_generated[i], lng_generated[i], color='b', marker='o')
        else:
            plt.plot(lat_generated[i], lng_generated[i], color='r', marker='o')


def find_max_min_coordinates(real, generated, trajectory):
    # logging.debug("converting JSON list to list for the library")
    # transform trajectory in lat and lng
    lat = []
    lng = []
    for el in trajectory:
        lat.append(el[0])
        lng.append(el[1])

    # transform real in lat and lng
    lat_real = []
    lng_real = []
    for el in real:
        lat_real.append(el[0])
        lng_real.append(el[1])

    # transform generated in lat and lng
    lat_generated = []
    lng_generated = []
    for el in generated:
        lat_generated.append(el[0])
        lng_generated.append(el[1])

    # logging.debug("plotting points")
    min_lat = []
    min_lat.append(np.amin(np.array(lat)))
    min_lat.append(np.amin(np.array(lat_real)))
    min_lat.append(np.amin(np.array(lat_generated)))
    real_total_min_lat = np.amin(np.array(min_lat))

    min_lon = []
    min_lon.append(np.amin(np.array(lng)))
    min_lon.append(np.amin(np.array(lng_real)))
    min_lon.append(np.amin(np.array(lng_generated)))
    real_total_min_lng = np.amin(np.array(min_lon))

    max_lat = []
    max_lat.append(np.amax(np.array(lat)))
    max_lat.append(np.amax(np.array(lat_real)))
    max_lat.append(np.amax(np.array(lat_generated)))
    real_total_max_lat = np.amax(np.array(max_lat))

    max_lon = []
    max_lon.append(np.amax(np.array(lng)))
    max_lon.append(np.amax(np.array(lng_real)))
    max_lon.append(np.amax(np.array(lng_generated)))
    real_total_max_lng = np.amax(np.array((max_lon)))

    return real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng


def how_many_folder(path):
    directories = os.listdir(path)
    if ".DS_Store" in directories:
        directories.remove(".DS_Store")

    list = []
    for el in directories:
        try:
            v = int(el)
            list.append(v)
        except:
            pass
    list.sort()

    return list


def how_many_fatherFolder(path):
    directories = os.listdir(path)
    if ".DS_Store" in directories:
        directories.remove(".DS_Store")

    list = []
    for el in directories:
        if ".py" not in el:
            list.append(el)

    return list

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

    # try:
    #     first_path = sys.argv[1]
    # except Exception as e:
    #     logging.debug("path, max_agent and max_classifier not passed. Program not going to work")
    #     sys.exit()

    first_path = "/Volumes/TheMaze/TuringLearning/january/latest/linear/"

    folders = how_many_fatherFolder(first_path)

    folders = ["Experiment-20top20top"]
    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)


        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            path = second_path + str(el) + "/"

            # if not os.path.exists(path + "_tmp00013.png"):
            names = []
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                    names.append(i)

            names = sorted_nicely(names)

            for name in names:
                # name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"
                numb = int(name.replace("trajectory-generatedPoints-", "").replace(".zip", "").split("-")[0])
                logging.debug("Analysing " + str(path) + str(name))
                trajectories_label, json_file = reanInfo(path + name)

                # manyTrajectories(json_file, trajectories_label, numb)

                plot_one_trajectory(trajectories_label, json_file, numb)

            # else:
            #     logging.debug("Pictures already present in the folder")

    logging.debug("End Program")
