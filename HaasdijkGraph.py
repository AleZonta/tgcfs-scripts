import logging
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame


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

    return total_agent, total_classifier


def printGraph(total):
    real_total_list = []
    for el in total[0][1]:
        sub_total = []
        for subel in el:
            sub_total.append(float(subel.replace(",", "")))
        sub_total = np.sort(sub_total)
        real_total_list.append(sub_total)

    columns = []
    for i in range(0, 100):
        test = []
        columns.append(test)

    # el is a row
    for el in real_total_list:
        # all the element in the row are different columns
        for i in range(0, len(el)):
            columns[i].append(el[i])

    x = {}
    for i in range(0, len(columns)):
        x[i] = columns[i]

    dfs = DataFrame(data=x)

    sns.set()

    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(dfs, vmin=0, xticklabels=5, yticklabels=10)
    ax.set_xlabel('population')
    ax.set_ylabel('generation')

    plt.show()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    total_agent, total_classifier = analise("/Users/alessandrozonta/Desktop/ex/v24")
    printGraph(total_agent)
    printGraph(total_classifier)

    logging.debug("End Program")
