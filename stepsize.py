import logging
import numpy as np
import matplotlib.pyplot as plt
from visPointGenNoGoogle import how_many_fatherFolder, how_many_folder
import seaborn as sns


def read_file(path):
    with open(path) as f:
        content = f.readlines()
        return content


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    first_path = "/Volumes/TheMaze/TuringLearning/february/today/"

    folders = how_many_fatherFolder(first_path)

    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)

        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            path = second_path + str(el) + "/"

            agents = read_file(path + "tgcfs.EA.Agents-stepsize.csv")
            classifiers = read_file(path + "tgcfs.EA.Classifiers-stepsize.csv")

            agents_array = []
            for el in agents:
                vect = el.replace("\n", "").replace("[", "").replace("]", "").split(",")
                real_vect = []
                for el in vect:
                    real_vect.append(float(el))
                agents_array.append(real_vect)

            classifiers_array = []
            for el in classifiers:
                vect = el.replace("\n", "").replace("[", "").replace("]", "").split(",")
                real_vect = []
                for el in vect:
                    real_vect.append(float(el))
                classifiers_array.append(real_vect)

            mean_agents = []
            std_agents = []
            min_agents = []
            max_agents = []
            for el in agents_array:
                np_array = np.array(el)
                mean_agents.append(np.mean(np_array))
                std_agents.append(np.std(np_array))
                min_agents.append(np.min(np_array))
                max_agents.append(np.max(np_array))

            mean_classifiers = []
            std_classifiers = []
            min_classifiers = []
            max_classifiers = []
            for el in classifiers_array:
                np_array = np.array(el)
                mean_classifiers.append(np.mean(np_array))
                std_classifiers.append(np.std(np_array))
                min_classifiers.append(np.min(np_array))
                max_classifiers.append(np.max(np_array))

            x = np.arange(0, len(agents_array))
            plt.figure(figsize=(12, 6))
            sns.set_style("darkgrid")
            # plt.plot(x, agents_array)
            # plt.plot(x, classifiers_array)
            plt.errorbar(x, mean_agents, std_agents, elinewidth=0.5 )
            # plt.errorbar(x, min_agents)
            # plt.errorbar(x, max_agents)
            plt.errorbar(x, mean_classifiers, std_classifiers, elinewidth=0.5)
            # plt.errorbar(x, min_classifiers)
            # plt.errorbar(x, max_classifiers)
            plt.xlabel("Generations")
            plt.ylabel("Step Size")
            # plt.legend(["Agents mean", "Agents min", "Agents max","Classifiers mean", "Classifiers min", "Classifiers max"])
            plt.legend(["Agents mean","Classifiers mean"])

            save_name = path + 'step_size.png'
            plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
            plt.close()
