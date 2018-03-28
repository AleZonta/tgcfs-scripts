from __future__ import print_function
import sys
import logging
import json
import zipfile
from pandas import np
import pandas as pd
import os
from math import sin, cos, sqrt, atan2, radians, degrees, fabs
import matplotlib.pyplot as plt
import seaborn as sns
import re
import tqdm


def single_elaboration(total, max):
    total_list_average = []
    total_list_std = []
    total_list_generation = []
    for experiment in total:
        gen = 0
        list_average = []
        list_std = []
        list_generation = []
        for generation in experiment[1]:
            lll = []
            for el in generation:
                lll.append(float(el.replace(",", "")))
            if len(lll) > 100:
                print("Be carefull, more than 100")
            list_average.append(np.average(np.array(lll)))
            list_std.append(np.std(np.array(lll)))
            list_generation.append(gen)
            gen += 1
        total_list_average.append(list_average)
        total_list_std.append(list_std)
        total_list_generation.append(list_generation)

    total_list_average_maybe = []
    total_list_std_maybe = []
    for i in range(len(total_list_average[0])):
        list_appo = []
        list_appo_two = []
        for j in range(len(total_list_average)):
            list_appo.append(total_list_average[j][i])
            list_appo_two.append(total_list_std[j][i])
        total_list_average_maybe.append(np.average(np.array(list_appo)))
        total_list_std_maybe.append(np.average(np.array(list_appo_two)))

    scaled_version = []
    for el in total_list_average_maybe:
        scaled_version.append((((el - 0) * (1 - 0)) / (max - 0)) + 0)
        # scaled_version.append(el)

    return scaled_version, total_list_generation[0]


def how_many_fatherFolder(path):
    directories = os.listdir(path)
    if ".DS_Store" in directories:
        directories.remove(".DS_Store")

    list = []
    for el in directories:
        if ".py" not in el:
            list.append(el)

    return list


def how_many_folder(path):
    directories = os.listdir(path)
    if ".DS_Store" in directories:
        directories.remove(".DS_Store")
    if "Figure_1.png" in directories:
        directories.remove("Figure_1.png")
    if "Figure_2.png" in directories:
        directories.remove("Figure_2.png")

    list = []
    for el in directories:
        try:
            v = str(el)
            list.append(v)
        except:
            pass
    list.sort()

    return list


def analise_single_folder(path, number, max_agent, max_classifier):
    total_agent = []
    name = path + "/" + str(number) + "/tgcfs.EA.Agents-fitness.csv"
    try:
        with open(name) as f:
            lis = [line.split() for line in f]
            lis = lis[1:]
            total_agent.append((number, lis))
    except Exception:
        pass

    total_classifier = []
    name = path + "/" + str(number) + "/tgcfs.EA.Classifiers-fitness.csv"
    try:
        with open(name) as f:
            lis = [line.split() for line in f]
            lis = lis[1:]
            total_classifier.append((number, lis))
    except Exception:
        pass

    scaled_version_agent, gen_agent = single_elaboration(total_agent, max_agent)
    scaled_version_classifier, gen_classifier = single_elaboration(total_classifier, max_classifier)

    ok = True
    if len(total_agent) > 1001:
        logging.debug("Folder " + number + "needs to be erased")
        ok = False

    return scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier, ok


def rean_info(path):
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


def compute_distance(lat1, lon1, lat2, lon2):
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


def compute_bearing(lat1, lon1, lat2, lon2):
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


def analise_distances(path, number, bigOrSmall):
    path = path + "/" + str(number) + "/"
    names = []
    for i in os.listdir(path):
        if bigOrSmall:
            name_to_check = "trajectory-generatedPoints-"
        else:
            name_to_check = "trajectory-generate-aSs-"
        # if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
        if os.path.isfile(os.path.join(path, i)) and name_to_check in i and ".zip" in i:
            names.append(i)

    names = sorted_nicely(names)


    numb = 0

    total_distances_angle = []
    total_distances = []

    logging.debug("Analysing Trajectories...")
    for i in tqdm.tqdm(range(len(names))):
        name = names[i]

        trajectories_label, json_file = rean_info(path + name)

        # ----------- distance bearings

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
            real_bearing = compute_bearing(lat_last[i], lng_last[i], lat_real[i], lng_real[i])

            # find index of the point generated corresponding to this trajectory
            index = [j for j, x in enumerate(label_generated) if x == label_real[i]]

            index_last_point = [j for j, x in enumerate(label_trajectory) if x == label_real[i]]

            distances = []
            for ind in index:
                bearing = compute_bearing(lat_last[index_last_point[0]], lng_last[index_last_point[0]],
                                         lat_generated[ind],
                                         lng_generated[ind])
                distances.append(fabs(bearing - real_bearing))
            array = np.array(distances)

            distance_per_trajectories.update({i: (np.max(array), np.min(array), np.mean(array), np.std(array), np.median(array))})
        total_distances_angle.append(distance_per_trajectories)

        # ----------- distance points

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
                distances.append(
                    float(compute_distance(lat_real[i], lng_real[i], lat_generated[ind], lng_generated[ind])))

            array = np.array(distances)
            distance_per_trajectories.update({i: (np.max(array), np.min(array), np.mean(array), np.std(array), np.median(array))})
        total_distances.append(distance_per_trajectories)

        numb += 1
    return total_distances, total_distances_angle


def find_max_values_fitness(path):
    fitness_file = path + "maxFitnessAchievable.txt"
    if os.path.exists(fitness_file):
        logging.debug("maxFitnessAchievable file is present, reading it")
        with open(fitness_file) as f:
            content = f.readlines()
            max_agent = int(content[0][19:-3])
            max_classifier = int(content[1][24:-3])
            return max_agent, max_classifier
    else:
        logging.debug("maxFitnessAchievable file not present, reading from config file")
        fitness_file = path + "tgcfs.Config.ReadConfig.txt"
        with open(fitness_file) as f:
            content = f.readlines()
            agent_pop = int(content[6][20:-2])
            agent_offspring = int(content[7][19:-2])
            classifier_pop = int(content[10][25:-2])
            classifier_offspring = int(content[11][24:-2])

            max_agent = agent_pop + agent_offspring
            max_classifier = (classifier_pop + classifier_offspring) * 2
            return max_agent, max_classifier


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # try:
    #     path = sys.argv[1]
    # except Exception as e:
    #     logging.debug("path non specified. Program not going to work")
    #     sys.exit()
    #
    # try:
    #     override = sys.argv[2]
    # except Exception as e:
    #     override = False

    # max_agent = 200
    # max_classifier = 400
    time_agent_more_classifier = 0
    first_path = "/Volumes/TheMaze/TuringLearning/tgcfs_lisa/"
    override = True
    # false means only the top 15 individual
    bigOrSmall = False

    folders = how_many_fatherFolder(first_path)

    # folders = ["Experiment-testLSTM"]

    problems = []

    # check all the external folder [name of the experiment]
    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        path = first_path + experiemnt + "/"

        res = how_many_folder(path)

        # res = ["0"]

        num_folder = len(res)

        logging.debug("Folder to analise -> " + str(num_folder))
        # check all the internal folder [number of the repetition]
        for folder in res:
            logging.debug("Analysing folder " + str(folder))
            max_agent, max_classifier = find_max_values_fitness(path + "/" + str(folder) + "/")
            logging.debug("Max fitness agent: " + str(max_agent) + ", Max fitness classifier: " + str(max_classifier))

            if bigOrSmall:
                real_path = path + "/" + str(folder) + "/" + "graph.png"
            else:
                real_path = path + "/" + str(folder) + "/" + "graphTop.png"
            create = True
            if not override:
                if os.path.exists(real_path):
                    create = False

            if create:

                # read the fitness and return it scaled 0-1
                logging.debug("Checking the fitness...")
                scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier, ok = analise_single_folder(
                    path,
                    folder,
                    max_agent,
                    max_classifier)

                if not ok:
                    problems.append((experiemnt, folder, "Problem with number of fitness values"))

                # read all the trajectories for the distance to the real point
                logging.debug("Checking the distances...")
                real_distances, real_distances_bearing = analise_distances(path, folder, bigOrSmall)

                x = []
                x = np.arange(0, len(real_distances))
                max_value = []
                min_value = []
                mean = []
                std = []
                for el in real_distances:
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
                    min_value.append(np.mean(np.array(b)))
                    mean.append(np.mean(np.array(c)))
                    std.append(np.mean(np.array(d)))

                # normalise distances
                max_median = 20
                median_norm = []
                std_norm = []
                max_value_norm = []
                min_value_norm = []
                for i in range(len(mean)):
                    median_norm.append((((mean[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)
                    std_norm.append((((std[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)
                    max_value_norm.append((((max_value[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)
                    min_value_norm.append((((min_value[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)

                x_bearing = []
                x_bearing = np.arange(0, len(real_distances_bearing))
                max_value_bearing = []
                min_value_bearing = []
                mean_bearing = []
                std_bearing = []
                for el in real_distances_bearing:
                    a = []
                    b = []
                    c = []
                    d = []
                    for k in el.keys():
                        a.append(el[k][0])
                        b.append(el[k][1])
                        c.append(el[k][2])
                        d.append(el[k][3])
                    max_value_bearing.append(np.mean(np.array(a)))
                    min_value_bearing.append(np.mean(np.array(b)))
                    mean_bearing.append(np.mean(np.array(c)))
                    std_bearing.append(np.mean(np.array(d)))

                # normalise distances
                max_median_b = 360.0
                mean_norm_b = []
                std_norm_b = []
                max_value_norm_b = []
                min_value_norm_b = []
                for i in range(len(mean_bearing)):
                    mean_norm_b.append((((mean_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)
                    std_norm_b.append((((std_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)
                    max_value_norm_b.append((((max_value_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)
                    min_value_norm_b.append((((min_value_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)

                plt.figure(figsize=(12, 6))
                sns.set_style("darkgrid")
                plt.errorbar(gen_agent, scaled_version_agent)
                plt.errorbar(gen_classifier, scaled_version_classifier)
                plt.errorbar(x, min_value_norm)
                plt.errorbar(x_bearing, min_value_norm_b)
                plt.xlabel("Generation")
                t = u"\u00b0"
                plt.ylabel("Fitness, Distance (MPD= " + str(max_median) + "m; MBD= " + str(max_median_b) + t + ")")
                plt.legend(("Agents", "Classifier", "Min Distance of the points generated from the real point",
                            "Min Difference of the real bearing from the bearing generated"))

                logging.debug("Saving graph")

                plt.savefig(real_path)
                # plt.show()

                plt.figure(figsize=(12, 6))
                sns.set_style("darkgrid")
                plt.errorbar(x, mean, std, elinewidth=0.5)
                plt.errorbar(x, min_value)
                plt.errorbar(x, max_value)
                plt.xlabel("Generation")
                t = u"\u00b0"
                plt.ylabel("Distance MPD")
                plt.legend(("Median", "Min", "Max"))

                logging.debug("Saving graph1")
                if bigOrSmall:
                    real_path = path + "/" + str(folder) + "/" + "graph1.png"
                else:
                    real_path = path + "/" + str(folder) + "/" + "graph1Top.png"
                plt.savefig(real_path)

                plt.figure(figsize=(12, 6))
                sns.set_style("darkgrid")
                plt.errorbar(x_bearing, mean_bearing, std_bearing, elinewidth=0.5)
                plt.errorbar(x, min_value_bearing)
                plt.errorbar(x, max_value_bearing)
                plt.xlabel("Generation")
                t = u"\u00b0"
                plt.ylabel("Distance MBD")
                plt.legend(("Median", "Min", "Max"))

                logging.debug("Saving graph2")
                if bigOrSmall:
                    real_path = path + "/" + str(folder) + "/" + "graph2.png"
                else:
                    real_path = path + "/" + str(folder) + "/" + "graph2Top.png"
                plt.savefig(real_path)


            else:
                logging.debug("Graph is already there")

    for el in problems:
        logging.debug(el)