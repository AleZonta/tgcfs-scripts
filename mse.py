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

    def print_graph(self, total_distances, path_where_to_save):
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

    def run(self):
        folders = how_many_fatherFolder(self.path)

        for experiemnt in folders:
            logging.debug("Folder under analysis -> " + str(experiemnt))
            second_path = self.path + experiemnt + "/"
            res = how_many_folder(second_path)
            num_folder = len(res)
            logging.debug("Folder to analise -> " + str(num_folder))

            for el in res:
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

                number_of_trajectories = pops.get_number_trajectories()
                total_distances = []
                numb = 0
                logging.debug("Analysing Trajectories...")
                for i in tqdm.tqdm(range(len(names))):
                    name = names[i]

                    # obtain info from the file
                    individuals = self.read_info(path_here + name)

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
                    total_distances.append(distance_per_trajectories)

                self.print_graph(total_distances, path_here)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.debug("Starting script")

    start_path = "/Volumes/TheMaze/TuringLearning/tgcfs_lisa/"

    program = Execute(start_path)
    program.run()