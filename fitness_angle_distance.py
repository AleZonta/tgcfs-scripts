import logging
import tqdm
import zipfile
import json
from visPointGenNoGoogle import how_many_folder, how_many_fatherFolder, find_max_fitnes, sorted_nicely
from visualiseNewPoints import Ind, Point, Population, Populations, Tra
import os
from pandas import np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import re


class DetailsPerGen(object):
    def __init__(self, vector, max_value):
        self.vector = np.array(vector)
        self.vector = (self.vector-0)/(max_value-0)
        self.mean = np.mean(self.vector)
        self.std = np.std(self.vector)


class Execute(object):
    def __init__(self, path):
        self.path = path

    def read_trajectory_info(self, local_path):
        with zipfile.ZipFile(local_path) as z:
            with z.open(z.namelist()[0]) as f:
                content = f.readlines()
                json_file = json.loads(content[0])
                trajectories = json_file["trajectories"]

                total_tra = []
                for trajectory in trajectories:
                    id = trajectory["id"]
                    points = trajectory["points"]
                    total_points = []
                    for p in points:
                        total_points.append(Point(p["Latitude"], p["Longitude"]))
                    total_tra.append(Tra(id, total_points))

                return total_tra

    def read_info(self, local_path):
        with zipfile.ZipFile(local_path) as z:
            with z.open(z.namelist()[0]) as f:
                content = f.readlines()

                json_file = json.loads(content[0])

                elements = json_file["size"]

                individuals = []

                for i in range(0, elements):
                    name = "trajectory-" + str(i)

                    info_individual = json_file[name]

                    generated_point = info_individual["generated"]
                    generated_points = []
                    for p in generated_point:
                        generated_points.append(Point(p["Latitude"], p["Longitude"]))

                    real_point = info_individual["real"]
                    real_points = []
                    for p in real_point:
                        real_points.append(Point(p["Latitude"], p["Longitude"]))

                    id = info_individual["id"]
                    classification = info_individual["classification"]

                    obj = Ind(id, classification, generated_points, real_points)
                    individuals.append(obj)

                return individuals

    def read_fitness(self,  local_path, max_agent, max_classifier):
        name = local_path + "/tgcfs.EA.Agents-fitness.csv"
        agent_generations_info = []
        classifier_generations_info = []

        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                agent_fitness = lis[1:]

                for generation in agent_fitness:
                    values = []
                    for val in generation:
                        values.append(float(val.replace(",", "")))
                    agent_generations_info.append(DetailsPerGen(values, max_agent))
        except Exception:
            pass

        name = local_path + "/tgcfs.EA.Classifiers-fitness.csv"
        try:
            with open(name) as f:
                lis = [line.split() for line in f]
                classifier_fitness = lis[1:]

                for generation in classifier_fitness:
                    values = []
                    for val in generation:
                        values.append(float(val.replace(",", "")))
                    classifier_generations_info.append(DetailsPerGen(values, max_classifier))
        except Exception:
            pass

        return agent_generations_info, classifier_generations_info

    def find_max_values_fitness(self, local_path):
        fitness_file = local_path + "maxFitnessAchievable.txt"
        if os.path.exists(fitness_file):
            logging.debug("maxFitnessAchievable file is present, reading it")
            with open(fitness_file) as f:
                content = f.readlines()
                max_agent = int(content[0][19:-3])
                max_classifier = int(content[1][24:-3])
                return max_agent, max_classifier
        else:
            logging.debug("maxFitnessAchievable file not present, reading from config file")
            fitness_file = local_path + "tgcfs.Config.ReadConfig.txt"
            with open(fitness_file) as f:
                content = f.readlines()
                agent_pop = int(content[6][20:-2])
                agent_offspring = int(content[7][19:-2])
                classifier_pop = int(content[10][25:-2])
                classifier_offspring = int(content[11][24:-2])

                max_agent = agent_pop + agent_offspring
                max_classifier = (classifier_pop + classifier_offspring) * 2
                return max_agent, max_classifier

    def print_graph_msd_per_trajectory(self, total_distances, path_where_to_save):
        df = DataFrame(columns=['gen', 'tra', "ind", 'distance'])

        i = 0
        number_of_trajectories = 0
        for el in total_distances:
            number_of_trajectories = len(el.keys())
            for k in el.keys():
                array = el[k]
                try:
                    q = len(array)
                    for qq in range(q):
                        d = {"gen": i, "tra": k, "ind": qq, "distance": array[qq]}
                        dfs = DataFrame(data=d, index=[i])
                        df = df.append(dfs)
                except Exception as e:
                    q = 1
                    for qq in range(q):
                        d = {"gen": i, "tra": k, "ind": qq, "distance": array}
                        dfs = DataFrame(data=d, index=[i])
                        df = df.append(dfs)


            i += 1
        sns.set_style("darkgrid")

        df = df[df.columns].astype(float)

        sns.lmplot(x="gen", y="distance", hue="tra", data=df, scatter_kws={"s": 1}, fit_reg=False)

        save_name = path_where_to_save + 'msd.png'
        plt.savefig(save_name, dpi=500, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
        plt.close()
        logging.debug("Graph saved!")

    def print_graph_msd_total(self, total_distance, std_distances, path_where_to_save):
        x = np.arange(len(names))
        plt.figure(figsize=(12, 6))
        sns.set_style("darkgrid")
        plt.errorbar(x, total_distance, std_distances, elinewidth=0.5)
        plt.xlabel("Generation")
        plt.ylabel("msd")

        # plt.show()
        plt.savefig(path_where_to_save + "/msds.png", dpi=500)
        plt.close()
        logging.debug("msds saved!")

    def print_fitnes(self, x, y_agent, std_agent, y_classifier, std_classifier,  path_where_to_save):
        plt.figure(figsize=(12, 6))
        sns.set_style("darkgrid")
        plt.errorbar(x, y_agent, std_agent)
        plt.errorbar(x, y_classifier, std_classifier)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.ylim(-0.05, 1.1)
        plt.legend(("Agents", "Classifier"))

        plt.savefig(path_where_to_save + "/fitness.png", dpi=500)
        plt.close()
        logging.debug("Fitness saved!")

    def run(self):
        folders = how_many_fatherFolder(self.path)
        folders = [s for s in folders if not re.search('txt',s)]
        folders = [s for s in folders if not re.search('jpg', s)]
        folders = [s for s in folders if not re.search('png', s)]

        for experiemnt in folders:
            logging.debug("Folder under analysis -> " + str(experiemnt))
            second_path = self.path + experiemnt + "/"
            res = how_many_folder(second_path)
            folders = [s for s in folders if not re.search('txt', s)]
            folders = [s for s in folders if not re.search('jpg', s)]
            folders = [s for s in folders if not re.search('png', s)]
            num_folder = len(res)
            logging.debug("Folder to analise -> " + str(num_folder))

            for el in res:
                logging.debug("Folder under analysis -> " + str(el))
                path_here = second_path + str(el) + "/"

                names = []
                for i in os.listdir(path_here):
                    if os.path.isfile(os.path.join(path_here, i)) and 'trajectory-generate-aSs-' in i and ".zip" in i:
                        names.append(i)

                names = sorted_nicely(names)

                pops = Populations()
                # find the trajectories ID and Points
                trajectories = self.read_trajectory_info(path_here + "trajectory.zip")
                for tra in trajectories:
                    pops.add_population(Population(tra))

                # analysing the fitness
                logging.debug("Analysing the fitness...")
                max_agent, max_classifier = self.find_max_values_fitness(path_here)
                agent_generations_info, classifier_generations_info = self.read_fitness(path_here, max_agent, max_classifier)

                x = np.arange(len(agent_generations_info))
                y_agent = []
                std_agent = []
                for element in agent_generations_info:
                    y_agent.append(element.mean)
                    std_agent.append(element.std)
                y_classifier = []
                std_classifier = []
                for element in classifier_generations_info:
                    y_classifier.append(element.mean)
                    std_classifier.append(element.std)

                # print fitnes
                self.print_fitnes(x, y_agent, std_agent, y_classifier, std_classifier,  path_here)

                total_distances = []
                total_distances_msd = []
                std_distances = []
                last_generations_values = []
                logging.debug("Analysing Trajectories...")
                for i in tqdm.tqdm(range(len(names))):
                    name = names[i]

                    # obtain info from the file
                    individuals = self.read_info(path_here + name)

                    if i == len(names) - 1:
                        for ind in individuals:
                            for el in ind.array:
                                last_generations_values.append(el)

                    msds = []
                    for ind in individuals:
                        msds.append(ind.MSD)
                    total_distances.append(np.mean(np.array(msds)))
                    std_distances.append(np.std(np.array(msds)))

                    # store the msd per trajectory
                    distance_per_trajectories = {}
                    for j in range(number_of_trajectories):
                        distances = []
                        for indiv in individuals:
                            if indiv.trajectoryID == pops.get_population(j).tra.trajectoryID:
                                distances.append(indiv.MSD)

                        array = np.array(distances)
                        MSD = (np.sum(array)) / len(array)
                        distance_per_trajectories.update({j: MSD})
                    total_distances_msd.append(distance_per_trajectories)

                # print graph msd per trajectory
                self.print_graph_msd_per_trajectory(total_distances_msd, path_here)

                # print graph total msd
                self.print_graph_msd_total(total_distance, std_distances, path_here)

                # save the last value
                array = np.array(last_generations_values)
                MSD = (np.sum(array)) / len(array)

                with open(path_here + "/MSD.txt", "w") as text_file:
                    text_file.write(str(MSD))

    def total_graph_mse(self):
        folders = how_many_fatherFolder(self.path)
        folders = [s for s in folders if not re.search('txt', s)]
        folders = [s for s in folders if not re.search('jpg', s)]
        folders = [s for s in folders if not re.search('png', s)]

        dfs = DataFrame(columns=['exp', 'neurones', 'MSD', "div"])
        index = 0
        for experiemnt in folders:
            logging.debug("Folder under analysis -> " + str(experiemnt))
            name_experiement = str(experiemnt).replace("Experiment-tgcfs-", "")
            second_path = self.path + experiemnt + "/"
            res = how_many_folder(second_path)
            res = [s for s in res if not re.search('txt', s)]
            res = [s for s in res if not re.search('jpg', s)]
            res = [s for s in res if not re.search('png', s)]
            res = sorted_nicely(res)
            num_folder = len(res)
            logging.debug("Folder to analise -> " + str(num_folder))

            for el in res:
                logging.debug("Folder under analysis -> " + str(el))
                path_here = second_path + str(el) + "/MSD.txt"
                tratt = str(el).replace("neurones", "")

                with open(path_here) as f:
                    content = f.readlines()

                    div = -1
                    if "ETH" in name_experiement:
                        div = 0
                    elif "G" in name_experiement:
                        div = 1
                    elif "I" in name_experiement:
                        div = 2

                    d = {"exp": name_experiement, "neurones": tratt, "MSD": float(content[0]), "div": div}
                    df = DataFrame(data=d, index=[index])
                    dfs = dfs.append(df)
                    index += 1

        sns.factorplot(x="exp", y="MSD", hue="neurones", data=dfs, kind="bar",
                       palette="muted")
        a = dfs.loc[dfs['div'] == 0]
        sns.factorplot(x="exp", y="MSD", hue="neurones", data=a, kind="bar",
                       palette="muted")
        a = dfs.loc[dfs['div'] == 1]
        sns.factorplot(x="exp", y="MSD", hue="neurones", data=a, kind="bar",
                       palette="muted")
        a = dfs.loc[dfs['div'] == 2]
        sns.factorplot(x="exp", y="MSD", hue="neurones", data=a, kind="bar",
                       palette="muted")
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.debug("Starting script")

    start_path = "/Volumes/TheMaze/TuringLearning/das5/"

    program = Execute(start_path)
    program.run()

    # program.total_graph_mse()