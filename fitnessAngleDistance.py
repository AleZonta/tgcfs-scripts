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

    if len(total_agent) > 1001:
        logging.debug("Folder " + number + "needs to be erased")

    return scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier


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
    #distance in metres
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


def analise_distances(path, number):
    path = path + "/" + str(number) + "/"
    files = 0
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
            files += 1

    max = files
    vect = np.arange(1, max + 1)
    real_distances = []
    real_distances_bearing = []
    arrays = []
    arrays_b = []
    for numb in vect:
        if numb%100 == 0:
            logging.debug("Analysing trajectory " + str(numb))

        name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"

        trajectories_label, json_file = rean_info(path + name)

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
            distances.append(float(compute_distance(lat_real[0], lng_real[0], lat_generated[i], lng_generated[i])))

        array = np.array(distances)
        # max_d = np.max(array)
        # distances_scaled_version = []
        # for el in distances:
        #     distances_scaled_version.append((((el - 0) * (1 - 0)) / (max_d - 0)) + 0)

        # array = np.array(distances_scaled_version)
        arrays.append(array)
        real_distances.append((np.max(array), np.min(array), np.mean(array), np.std(array)))


        # last point trajectory
        lat_last = []
        lng_last = []
        for el in json_file[trajectories_label[0]]["trajectory"]:
            lat_last.append(el[0])
            lng_last.append(el[1])

        real_bearing = compute_bearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_real[0], lng_real[0])

        distances_bearing = []
        # compute distance
        for i in range(len(lat_generated)):
            # compute the distances
            bearing = compute_bearing(lat_last[len(lat_last) -1], lng_last[len(lat_last) -1], lat_generated[i], lng_generated[i])
            distances_bearing.append(fabs(real_bearing - bearing))

        array_b = np.array(distances_bearing)
        # max_d = np.max(array)
        # distances_bearing_scaled_version = []
        # for el in distances_bearing:
        #     distances_bearing_scaled_version.append((((el - 0) * (1 - 0)) / (max_d - 0)) + 0)

        # array = np.array(distances_bearing_scaled_version)
        arrays_b.append(array_b)
        real_distances_bearing.append((np.max(array_b), np.min(array_b), np.mean(array_b), np.std(array_b)))

    return real_distances, real_distances_bearing


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

    try:
        path = sys.argv[1]
    except Exception as e:
        logging.debug("path non specified. Program not going to work")
        sys.exit()

    try:
        override = sys.argv[2]
    except Exception as e:
        override = False



    # max_agent = 200
    # max_classifier = 400
    time_agent_more_classifier = 0
    # path = "/Users/alessandrozonta/Desktop/"

    res = how_many_folder(path)

    # res = ["23 ni++"]
    num_folder = len(res)
    logging.debug("Folder to analise -> " + str(num_folder))

    for folder in res:
        logging.debug("Analysing folder " + str(folder))
        max_agent, max_classifier = find_max_values_fitness(path + "/" + str(folder) + "/")
        logging.debug("Max fitness agent: " + str(max_agent) + ", Max fitness classifier: " + str(max_classifier))

        real_path = path + "/" + str(folder) + "/" + "graph.png"
        create = True
        if not override:
            if os.path.exists(real_path):
                create = False

        if create:

            # read the fitness and return it scaled 0-1
            logging.debug("Checking the fitness")
            scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier = analise_single_folder(path, folder, max_agent, max_classifier)

            # read all the trajectories for the distance to the real point
            logging.debug("Checking the distances")
            real_distances, real_distances_bearing = analise_distances(path, folder)


            x = []
            mean = []
            std = []
            x = np.arange(0, len(real_distances))
            for el in real_distances:
                mean.append(el[2])
                std.append(el[3])


            # normalise distances
            max_median = 1.5
            median_norm = []
            std_norm = []

            for i in range(len(mean)):
                median_norm.append((((mean[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)
                std_norm.append((((std[i] - 0) * (1 - 0)) / (max_median - 0)) + 0)

            x_bearing = []
            median_bearing = []
            std_bearing = []
            x_bearing = np.arange(0, len(real_distances_bearing))
            for el in real_distances_bearing:
                median_bearing.append(el[2])
                std_bearing.append(el[3])


            # normalise distances
            max_median_b = 360.0
            median_norm_b = []
            std_norm_b = []

            for i in range(len(median_bearing)):
                median_norm_b.append((((median_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)
                std_norm_b.append((((std_bearing[i] - 0) * (1 - 0)) / (max_median_b - 0)) + 0)

            plt.figure(figsize=(12, 6))
            sns.set_style("darkgrid")
            plt.errorbar(gen_agent, scaled_version_agent)
            plt.errorbar(gen_classifier, scaled_version_classifier)
            plt.errorbar(x, median_norm, std_norm, elinewidth=0.5)
            plt.errorbar(x_bearing, median_norm_b, std_norm_b, elinewidth=0.5)
            plt.xlabel("Generation")
            t = u"\u00b0"
            plt.ylabel("Fitness, Distance (MPD= " + str(max_median) + "m; MBD= " + str(max_median_b) + t +")")
            plt.legend(("Agents", "Classifier", "Distance of the points generated from the real point", "Difference of the real bearing from the bearing generated"))

            logging.debug("Saving graph")

            plt.savefig(real_path)
        else:
            logging.debug("Graph is already there")

