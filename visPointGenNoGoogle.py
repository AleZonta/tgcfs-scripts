import sys
import logging
import zipfile
import os
import json
from pandas import np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import tqdm



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


def plot_one_trajectory(trajectories_label, json_file, numb, max, real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng):
    # real_total_min_lat = 52.045906899999999
    # real_total_min_lng = 4.331558
    # real_total_max_lat = 52.045942
    # real_total_max_lng = 4.3316090999999997
    # real_total_min_lat = 52.0422
    # real_total_min_lng = 4.31475
    # real_total_max_lat = 52.0427
    # real_total_max_lng = 4.3155

    # logging.debug("Computing graph " + str(numb))

    plt.figure(figsize=(10, 8))

    for ell in trajectories_label:
        printTrajectory(json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"],
                        real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng, plt,
                        json_file[ell]["classification"], max)

    plt.colorbar()
    save_name = path + '_tmp%05d.png' % numb
    plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
    plt.close()


def printTrajectory(real, generated, trajectory, real_total_min_lat, real_total_min_lng, real_total_max_lat,
                    real_total_max_lng, plt, fitness, max):
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

    plt.axis([real_total_min_lat, real_total_max_lat, real_total_min_lng, real_total_max_lng])

    # print trajectory
    plt.plot(lat, lng, color='b', marker='o')

    # print real point
    plt.plot(lat_real, lng_real, color='k', marker='o')

    # print generated point
    # for i in range(len(lat_generated)):
    plt.scatter(lat_generated, lng_generated, c=[fitness], marker='o', vmin=0., vmax=max, cmap='autumn')


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


def find_max_fitnes(path):
    name = path + "tgcfs.EA.Agents-fitness.csv"
    try:
        with open(name) as f:
            lis = [line.split() for line in f]
            lis = lis[1:]
            # need to find all the last position
            fit = []
            for el in lis:
                fit.append(float(el[len(el) - 1].replace(",","")))

            max_finale = np.amax(np.array(fit))
            value = np.ceil(max_finale)
            return value

    except Exception:
        pass


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

    first_path = "/Volumes/TheMaze/TuringLearning/january/newFitness/uvaok/"

    folders = how_many_fatherFolder(first_path)

    folders = ["Experiment-plusplusHoF"]

    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)

        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            path = second_path + str(el) + "/"

            # check max fitness achiavable
            maxx = find_max_fitnes(path)

            # if not os.path.exists(path + "_tmp00013.png"):
            names = []
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                    names.append(i)

            names = sorted_nicely(names)

            logging.debug("Finding boundaries...")
            # checking only 1/4 of all the trajectory in order to find the boudaries

            total_checked_folder = len(names) / 4
            total_min_lat = []
            total_min_lng = []
            total_max_lat = []
            total_max_lng = []
            for i in tqdm.tqdm(range(total_checked_folder)):
                name = names[i]
                trajectories_label, json_file = reanInfo(path + name)

                for ell in trajectories_label:
                    real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng = find_max_min_coordinates(json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"])
                    total_min_lat.append(real_total_min_lat)
                    total_min_lng.append(real_total_min_lng)
                    total_max_lat.append(real_total_max_lat)
                    total_max_lng.append(real_total_max_lng)

            min_lat = np.amin(np.array(total_min_lat)) - 0.0001
            min_lng = np.amin(np.array(total_min_lng)) - 0.0001
            max_lat = np.amax(np.array(total_max_lat)) + 0.0001
            max_lng = np.amax(np.array(total_max_lng)) + 0.0001

            logging.debug("Boundaries found!")

            logging.debug("Creating graphs...")
            for i in tqdm.tqdm(range(len(names))):
                name = names[i]
                # name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"
                numb = int(name.replace("trajectory-generatedPoints-", "").replace(".zip", "").split("-")[0])
                # logging.debug("Analysing " + str(path) + str(name))
                trajectories_label, json_file = reanInfo(path + name)

                # manyTrajectories(json_file, trajectories_label, numb)

                plot_one_trajectory(trajectories_label, json_file, numb, maxx, min_lat, min_lng, max_lat, max_lng)

                # else:
                #     logging.debug("Pictures already present in the folder")
            logging.debug("Graphs created!")
    logging.debug("End Program")
