import logging
from fitnessAngleDistance import how_many_folder
import subprocess
import os
import fnmatch
import shutil
from pandas import np
from visPointGenNoGoogle import how_many_folder


def download_graphs_from_all(path_here, path_on_server, name_server, folder_name):
    number_folder = 35
    what_to_copy = ["graph.png", "graph1.png", "graph2.png", "movie.mp4"]
    folders = np.arange(0, number_folder + 1)

    for el in folders:
        logging.debug("Analysing folder " + str(el))
        for file in what_to_copy:
            remote_path = path_on_server + folder_name + "/" + str(el) + "/" + file
            bashCommand = "scp " + name_server + ":" + remote_path + " ."

            directory = path_here + folder_name
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
            directory = path_here + folder_name + "/" + str(el)
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)

            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=directory)
            output, error = process.communicate()

            logging.debug("Copied " + str(file))


def download_other_file_in_best_folder(path_here, path_on_server, name_server, folder_name):
    folders = how_many_folder(path_here + "/" + folder_name)
    what_to_copy = ["classifier.log", "tgcfs.Config.ReadConfig.txt", "movie.mp4"]

    for el in folders:
        logging.debug("Analysing folder " + str(el))

        for file in what_to_copy:

            remote_path = path_on_server + folder_name + "/" + str(el) + "/" + file
            bashCommand = "scp " + name_server + ":" + remote_path + " ."

            directory = path_here + folder_name
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)
            directory = path_here + folder_name + "/" + str(el)
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)

            if not os.path.exists(directory + "/" + file):

                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=directory)
                output, error = process.communicate()

                logging.debug("Copied " + str(file))
            else:
                logging.debug(file + " -> file not copied, already there")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path_here = "/Users/alessandrozonta/Desktop/"
    path_on_server = "/Volumes/TheMaze/TuringLearning/january/"
    name_server = "alessandro@145.108.189.129"

    folder_name = "das5"

    download_other_file_in_best_folder(path_here, path_on_server, name_server, folder_name)