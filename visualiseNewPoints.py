import logging
import zipfile
import json
import os
import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import np
from visPointGenNoGoogle import how_many_folder, how_many_fatherFolder, find_max_fitnes, sorted_nicely


class Tra(object):
    def __init__(self, trajectoryID, points):
        self.trajectoryID = trajectoryID
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.xs = []
        self.ys = []
        # compute max and minimum of the trajectory
        for el in points:
            self.xs.append(el.x)
            self.ys.append(el.y)
        self.max_x = np.amax(np.array(self.xs))
        self.min_x = np.amin(np.array(self.xs))
        self.max_y = np.amax(np.array(self.ys))
        self.min_y = np.amin(np.array(self.ys))


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ind(object):
    def __init__(self, trajectoryID, classification, generetedPoint, realPoint):
        self.trajectoryID = trajectoryID
        self.classification = classification
        self.generetedPoint = generetedPoint
        self.realPoint = realPoint
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.xs_real = []
        self.ys_real = []
        self.xs_generated = []
        self.ys_generated = []

        # compute max and minimum of the individual
        xs = []
        ys = []
        for el in self.realPoint:
            xs.append(el.x)
            ys.append(el.y)
            if el.x not in self.xs_real:
                self.xs_real.append(el.x)
            if el.y not in self.ys_real:
                self.ys_real.append(el.y)
        for el in self.generetedPoint:
            xs.append(el.x)
            ys.append(el.y)
            if el.x not in self.xs_generated:
                self.xs_generated.append(el.x)
            if el.y not in self.ys_generated:
                self.ys_generated.append(el.y)
        self.max_x = np.amax(np.array(xs))
        self.min_x = np.amin(np.array(xs))
        self.max_y = np.amax(np.array(ys))
        self.min_y = np.amin(np.array(ys))

        # compute mse points this trajectory
        distances = []
        for i in range(len(self.generetedPoint)):
            a = np.array((self.xs_real[i], self.ys_real[i]))
            b = np.array((self.xs_generated[i], self.ys_generated[i]))
            value = np.linalg.norm(a - b) * 100000
            distances.append(pow(value, 2))

        self.array = np.array(distances)
        self.MSD = (np.sum(self.array)) / len(self.array)


class Population(object):
    def __init__(self, tra):
        self.tra = tra
        self.max_x = []
        self.max_y = []
        self.min_x = []
        self.min_y = []
        self.max_x.append(self.tra.max_x)
        self.max_y.append(self.tra.max_y)
        self.min_x.append(self.tra.min_x)
        self.min_y.append(self.tra.min_y)

    def add_individual(self, ind):
        self.max_x.append(ind.max_x)
        self.max_y.append(ind.max_y)
        self.min_x.append(ind.min_x)
        self.min_y.append(ind.min_y)

    def get_max_x(self):
        return np.amax(np.array(self.max_x)) + 0.000001

    def get_max_y(self):
        return np.amax(np.array(self.max_y)) + 0.000001

    def get_min_x(self):
        return np.amin(np.array(self.min_x)) - 0.000001

    def get_min_y(self):
        return np.amin(np.array(self.min_y)) - 0.000001


class Populations(object):
    def __init__(self):
        self.populs = []

    def add_population(self, pop):
        self.populs.append(pop)

    def get_pop_id(self, id):
        i = 0
        while self.populs[i].tra.trajectoryID != id:
            i += 1
        return self.populs[i]

    def get_number_trajectories(self):
        return len(self.populs)

    def get_population(self, number):
        return self.populs[number]


class Execute(object):
    def __init__(self, path, printingOnlyLastPic, howManyLastPic, name_to_check):
        self.path = path
        self.printingOnlyLastPic = printingOnlyLastPic
        self.howManyLastPic = howManyLastPic
        self.name_to_check = name_to_check

    def read_trajectory_info(self, path):
        with zipfile.ZipFile(path) as z:
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

    def read_info(self, path):
        with zipfile.ZipFile(path) as z:
            with z.open(z.namelist()[0]) as f:
                content = f.readlines()

                json_file = json.loads(content[0])

                elements = json_file["size"]

                individuals = []

                for i in range(0, elements):
                    name = "trajectory-" + str(i)

                    infoIndividual = json_file[name]

                    generatedPoint = infoIndividual["generated"]
                    generatedPoints = []
                    for p in generatedPoint:
                        generatedPoints.append(Point(p["Latitude"], p["Longitude"]))

                    realPoint = infoIndividual["real"]
                    realPoints = []
                    for p in realPoint:
                        realPoints.append(Point(p["Latitude"], p["Longitude"]))

                    id = infoIndividual["id"]
                    classification = infoIndividual["classification"]

                    obj = Ind(id, classification, generatedPoints, realPoints)
                    individuals.append(obj)

                return individuals

    def print_trajectory(self, individuals, pops, numbs, max_fitness, path):
        plt.figure(figsize=(12, 8))
        plt.autoscale(enable=False, tight=True)
        # sns.set_style("darkgrid")

        number_of_trajectories = pops.get_number_trajectories()

        for i in range(number_of_trajectories):
            j = i + 1
            if number_of_trajectories == 1:
                plt.subplot(1, 1, j)
            elif number_of_trajectories == 2:
                plt.subplot(1, 2, j,)
            elif number_of_trajectories == 3:
                plt.subplot(1, 3, j)
            elif number_of_trajectories == 5:
                plt.subplot(2, 3, j)
            elif number_of_trajectories == 6:
                plt.subplot(2, 3, j)
            elif number_of_trajectories == 10:
                plt.subplot(3, 4, j)
            elif number_of_trajectories == 20:
                plt.subplot(4, 5, j)
            elif number_of_trajectories == 25:
                plt.subplot(5, 5, j)
            elif number_of_trajectories == 30:
                plt.subplot(5, 6, j)
            elif number_of_trajectories == 40:
                plt.subplot(6, 7, j)
            else:
                raise Exception("Num trajectories not set")

            population = pops.get_population(i)

            # find the boundaries
            # logging.debug([population.get_min_x(), population.get_max_x(), population.get_min_y(), population.get_max_y()])
            if number_of_trajectories == 1:
                plt.axis([population.get_min_x(), population.get_max_x(), population.get_min_y(), population.get_max_y()])
            plt.axis('off')

            # current trajectory
            current_trajectory = population.tra
            latitude_trajectory = current_trajectory.xs
            longitude_trajecotry = current_trajectory.ys
            plt.plot(latitude_trajectory, longitude_trajecotry, color='b', marker='o', markersize=1)

            # real points
            # find individual for the current trajectory
            latitude_real_points = []
            longitude_real_points = []
            latitude_generated_points = []
            longitude_generated_points = []
            classification_individuals = []
            for inds in individuals:
                if inds.trajectoryID == current_trajectory.trajectoryID:
                    for el in inds.xs_real:
                        if el not in latitude_real_points:
                            latitude_real_points.append(el)
                    for el in inds.ys_real:
                        if el not in longitude_real_points:
                            longitude_real_points.append(el)
                    for el in inds.xs_generated:
                        if el not in latitude_generated_points:
                            latitude_generated_points.append(el)
                    for el in inds.ys_generated:
                        if el not in longitude_generated_points:
                            longitude_generated_points.append(el)
                    for el in inds.ys_generated:
                        classification_individuals.append(inds.classification)

            # i do not want lines, only dots
            for j in range(len(latitude_real_points)):
                plt.plot(latitude_real_points[j], longitude_real_points[j], color='k', marker='o', markersize=1)

            if len(latitude_generated_points) != len(longitude_generated_points):
                logging.debug("problem in generating the pic")
                pass
            # generated points
            plt.scatter(latitude_generated_points, longitude_generated_points, c=[classification_individuals], marker='o', vmin=0., vmax=max_fitness, cmap='autumn', s=1)
            # plt.show()

        save_name = path + '_tmp%05d.png' % numbs
        plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None, )
        plt.close()

    def print_trajectories_each_in_graph(self, individuals, pops, numbs, max_fitness, path):

        # sns.set_style("darkgrid")

        number_of_trajectories = pops.get_number_trajectories()
        for i in tqdm.tqdm(range(number_of_trajectories)):
            plt.figure(figsize=(12, 8))
            plt.autoscale(enable=False, tight=True)
            population = pops.get_population(i)
            plt.axis([population.get_min_x(), population.get_max_x(), population.get_min_y(), population.get_max_y()])
            plt.axis('off')

            # current trajectory
            current_trajectory = population.tra
            latitude_trajectory = current_trajectory.xs
            longitude_trajecotry = current_trajectory.ys
            plt.plot(latitude_trajectory, longitude_trajecotry, color='b', marker='o', markersize=1)

            # real points
            # find individual for the current trajectory
            latitude_real_points = []
            longitude_real_points = []
            latitude_generated_points = []
            longitude_generated_points = []
            classification_individuals = []
            for inds in individuals:
                if inds.trajectoryID == current_trajectory.trajectoryID:
                    for el in inds.xs_real:
                        if el not in latitude_real_points:
                            latitude_real_points.append(el)
                    for el in inds.ys_real:
                        if el not in longitude_real_points:
                            longitude_real_points.append(el)
                    for el in inds.xs_generated:
                        if el not in latitude_generated_points:
                            latitude_generated_points.append(el)
                    for el in inds.ys_generated:
                        if el not in longitude_generated_points:
                            longitude_generated_points.append(el)
                    for el in inds.ys_generated:
                        classification_individuals.append(inds.classification)

            # i do not want lines, only dots
            for j in range(len(latitude_real_points)):
                plt.plot(latitude_real_points[j], longitude_real_points[j], color='k', marker='o', markersize=1)

            # generated points
            plt.scatter(latitude_generated_points, longitude_generated_points, c=[classification_individuals],
                        marker='o', vmin=0., vmax=max_fitness, cmap='autumn', s=1)
            # plt.show()

            save_name = path + '_tra%05d.png' % i
            plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None, )
            plt.close()

    def run(self, one_tra_per_graph, f, n):
        folders = how_many_fatherFolder(self.path)
        if len(f) > 0:
            folders = f

        for experiemnt in folders:
            logging.debug("Folder under analysis -> " + str(experiemnt))
            second_path = first_path + experiemnt + "/"
            res = how_many_folder(second_path)

            if len(n) > 0:
                res = n

            num_folder = len(res)
            logging.debug("Folder to analise -> " + str(num_folder))

            for el in res:
                path = second_path + str(el) + "/"
                logging.debug("Folder under analysis -> " + str(el))


                # check max fitness achiavable
                max_fitness = find_max_fitnes(path)
                if max_fitness is None:
                    max_fitness = 500

                pops = Populations()
                # find the trajectories ID and Points
                trajectories = self.read_trajectory_info(path + "trajectory.zip")
                for tra in trajectories:
                    pops.add_population(Population(tra))


                pictures = []
                for i in os.listdir(path):
                    if os.path.isfile(os.path.join(path, i)) and "_tmp0" in i and ".png" in i:
                        pictures.append(i)
                # if (len(pictures)) > 700:
                #     logging.debug("Pictures already available, skipping the folder")
                #     break

                # count how many generation I have and find name files storing it
                names = []
                for i in os.listdir(path):
                    if os.path.isfile(os.path.join(path, i)) and self.name_to_check in i and ".zip" in i:
                        names.append(i)
                names = sorted_nicely(names)

                if len(names) == 0:
                    logging.debug("No files to generate")
                    break

                # keep only last pic
                if self.printingOnlyLastPic:
                    names = names[-self.howManyLastPic:]

                # load all the info to make the boundaries
                logging.debug("Loading Information...")

                for i in tqdm.tqdm(range(len(names))):
                    name = names[i]
                    individuals = self.read_info(path + name)

                    for ind in individuals:
                        pop = pops.get_pop_id(ind.trajectoryID)
                        pop.add_individual(ind)

                logging.debug("Generating Graphs...")

                # now I have all the individuals in the populations
                if one_tra_per_graph:
                    name = names[0]
                    numb = 0
                    indivi = self.read_info(path + name)
                    self.print_trajectories_each_in_graph(indivi, pops, numb, max_fitness, path)
                else:
                    for i in tqdm.tqdm(range(len(names))):
                        name = names[i]
                        numb = int(name.replace(name_to_check, "").replace(".zip", "").split("-")[0])

                        indivi = self.read_info(path + name)

                        self.print_trajectory(indivi, pops, numb, max_fitness, path)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # ----------- details -----------------
    first_path = "/Users/alessandrozonta/Desktop/"
    folder = ["Experiment-testTra"]
    res = ["2"]
    printingOnlyLastPic = False
    howManyLastPic = 150
    name_to_check = "trajectory-generate-aSs-"
    name_to_check = "trajectory-generatedPoints-"
    one_tra_per_graph = True
    # --------- end details ---------------

    program = Execute(first_path, printingOnlyLastPic, howManyLastPic, name_to_check)
    program.run(one_tra_per_graph, folder, res)


