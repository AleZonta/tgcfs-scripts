import logging
import numpy as np
import matplotlib.pyplot as plt


def read_file(path):
    with open(path) as f:
        content = f.readlines()
        return content


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    first_path = "/Volumes/TheMaze/TuringLearning/january/sigmoid/Experiment-plusplus/0/"

    agents = read_file(first_path + "tgcfs.EA.Agents-stepsize.csv")
    classifiers = read_file(first_path + "tgcfs.EA.Classifiers-stepsize.csv")


    agents_array = []
    for el in agents:
        agents_array.append(float(el.replace("\n","").replace("[","").replace("]","")))

    classifiers_array = []
    for el in classifiers:
        classifiers_array.append(float(el.replace("\n", "").replace("[", "").replace("]", "")))


    x = np.arange(0, len(agents_array))

    plt.plot(x, agents_array)
    plt.plot(x, classifiers_array)
    plt.xlabel("Generations")
    plt.ylabel("Step Size")
    plt.legend(["Agents", "Classifiers"])
    plt.show()
