import os

import logging
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import numpy as np

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

    return scaled_version, total_list_generation[0]


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

    return scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier





if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    max_agent = 200
    max_classifier = 400
    time_agent_more_classifier = 0

    scaled_version_agent, gen_agent, scaled_version_classifier, gen_classifier = analise_single_folder(path, res[0], max_agent, max_classifier)