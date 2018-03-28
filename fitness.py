# main
import os

import logging
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import numpy as np
from visPointGenNoGoogle import how_many_fatherFolder


def analise(path, one, max_agent, max_classifier):
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


    total = []
    for el in list:
        if one:
            name = path + "/" + str(el) + "/tgcfs.EA.Agents-fitness.csv"
        else:
            name = path + "/" + str(el) + "/tgcfs.EA.Classifiers-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                total.append((el, lis))
        except Exception:
            pass

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
                lll.append(int(el.replace(",","")))
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


    # normalise with the maximum value

    scaled_version = []
    for el in total_list_average_maybe:
        if one:
            scaled_version.append((((el - 0) * (1 - 0)) / (max_agent - 0)) + 0)
        else:
            scaled_version.append((((el - 0) * (1 - 0)) / (max_classifier - 0)) + 0)
   # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

    plt.figure()
    plt.errorbar(total_list_generation[0], scaled_version)
    plt.show()




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

    # scaled_version = []
    # for el in total_list_average_maybe:
    #         scaled_version.append((((el - 0) * (1 - 0)) / (max - 0)) + 0)

    return total_list_average_maybe,total_list_std_maybe, total_list_generation[0]


def analise_both(path, max_agent, max_classifier):
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

    total_agent = []
    for el in list:
        name = path + "/" + str(el) + "/tgcfs.EA.Agents-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                total_agent.append((el, lis))
        except Exception:
            pass

    total_classifier = []
    for el in list:
        name = path + "/" + str(el) + "/tgcfs.EA.Classifiers-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                total_classifier.append((el, lis))
        except Exception:
            pass

    scaled_version_agent, gen_agent = single_elaboration(total_agent, max_agent)
    scaled_version_classifier, gen_classifier = single_elaboration(total_classifier, max_classifier)

    plt.figure()
    plt.errorbar(gen_agent, scaled_version_agent)
    plt.errorbar(gen_classifier, scaled_version_classifier)
    plt.ylim(0, 1)
    plt.xlabel("Generation")
    plt.ylabel("Fitness (0->1)")
    plt.legend(("Agents", "Classifier"))
    plt.show()


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


def analise_both_single_folder(path, max_agent, max_classifier):
    total_agent = []
    name = path + "/tgcfs.EA.Agents-fitness.csv"
    try:
        with open(name) as f:
            lis = [line.split() for line in f]
            lis = lis[1:]
            total_agent.append((max_classifier, lis))
    except Exception:
        name = path + "/EA.Agents-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                total_agent.append((max_classifier, lis))
        except Exception:
            logging.debug("Problem lines")
    # total_classifier = []
    # name = path + "/" + str(number) + "/tgcfs.EA.Classifiers-fitness.csv"
    # try:
    #     with open(name) as f:
    #         lis = [line.split() for line in f]
    #         lis = lis[1:]
    #         total_classifier.append((number, lis))
    # except Exception:
    #     pass

    scaled_version_agent, std, gen_agent = single_elaboration(total_agent, max_agent)
    # scaled_version_classifier, gen_classifier = single_elaboration(total_classifier, max_classifier)

    plt.figure()
    sns.set_style("darkgrid")

    plt.errorbar(gen_agent, scaled_version_agent, std)
    # plt.errorbar(gen_classifier, scaled_version_classifier)
    # plt.ylim(-40, 2)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(("Agents"))
    plt.show()



def combined_fitness(path):
    folders = how_many_fatherFolder(path)

    if "Figure_0.png" in folders:
        folders.remove("Figure_0.png")

    plt.figure()
    sns.set_style("darkgrid")

    for folder in folders:
        second_path = path + folder + "/"
        res = how_many_folder(second_path)

        for numb in res:
            total_agent = []
            name = second_path + str(numb) + "/tgcfs.EA.Agents-fitness.csv"
            try:
                with open(name) as f:
                    lis = [line.split() for line in f]
                    lis = lis[1:]
                    total_agent.append((max_classifier, lis))
            except Exception:
                name = path + "/EA.Agents-fitness.csv"
                try:
                    with open(name) as f:
                        lis = [line.split() for line in f]
                        total_agent.append((max_classifier, lis))
                except Exception:
                    logging.debug("Problem lines")
            scaled_version_agent, std, gen_agent = single_elaboration(total_agent, max_agent)
            plt.errorbar(gen_agent, scaled_version_agent, std)

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.ylim(-8, 0.2)
    plt.legend(folders)
    plt.show()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    max_agent = 0
    max_classifier = 0
    time_agent_more_classifier = 0
    # one = True  # agent
    # # one = False  # classifier
    # analise("/Users/alessandrozonta/Desktop/res", one, max_agent, max_classifier)
    # analise_both("/Users/alessandrozonta/Desktop/tl-idsa-tot/results/Experiment-Virulance", max_agent, max_classifier, time_agent_more_classifier)

    # path = "/Volumes/TheMaze/TuringLearning/march/22march/Experiment-lstm-Inc-Two-Ten-Neurons-ETH/2/"
    # res = how_many_folder(path)
    #
    # analise_both_single_folder(path, max_agent, max_classifier)

    combined_fitness("/Volumes/TheMaze/TuringLearning/march/OnlyGenerator/More Points/")

    logging.debug("End Program")
