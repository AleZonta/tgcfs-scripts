import logging
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

# reading the file with the fitness for the agent and the classifiers given by input
# read only one file per time, no more experiment for the same setting
def analise(path):
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
                lis = lis[1:]
                total_agent.append((el, lis))
        except Exception:
            pass

    total_classifier = []
    for el in list:
        name = path + "/" + str(el) + "/tgcfs.EA.Classifiers-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                lis = lis[1:]
                total_classifier.append((el, lis))
        except Exception:
            pass

    return total_agent, total_classifier


def printGraph(total, number):
    real_total_list = []
    for el in total[number][1]:
        sub_total = []
        for subel in el:
            sub_total.append(float(subel.replace(",", "")))
        sub_total = np.sort(sub_total)
        real_total_list.append(sub_total)

    columns = []
    for i in range(0, 10):
        test = []
        columns.append(test)

    # el is a row
    for el in real_total_list:
        # all the element in the row are different columns
        try:
            for i in range(0, len(el)):
                columns[i].append(el[i])
        except Exception:
            pass

    x = {}
    for i in range(0, len(columns)):
        x[i] = columns[i]

    dfs = DataFrame(data=x)

    sns.set()

    plt.figure(number)
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dfs, vmin=0, xticklabels=5, yticklabels=30, cmap="RdBu_r")
    ax.set_xlabel('population')
    ax.set_ylabel('generation')




if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    total_agent, total_classifier = analise("/Volumes/TheMaze/TuringLearning/SIKS/")

    logging.debug("there are " + str(len(total_agent)) + " different results in this folder")

    for i in range(len(total_agent)):
        logging.debug("showing " + str(i))
        printGraph(total_agent, i)
        printGraph(total_classifier, i)

    plt.show()
    logging.debug("End Program")
