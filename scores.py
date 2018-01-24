from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import json
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import os
import re


from pandas import DataFrame, np


def transform(value, max_old, min_old, max_new, min_new):
    return (max_new - min_new) * ((value - min_old) / (max_old - min_old)) + min_new


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


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # try:
    #     realpath = sys.argv[1]
    # except Exception as e:
    #     logging.debug("path, max_agent and max_classifier not passed. Program not going to work")
    #     sys.exit()

    realpath = "/Volumes/TheMaze/TuringLearning/january/latest/linear/Experiment-plusplus/"

    res = how_many_folder(realpath)
    num_folder = len(res)
    logging.debug("Folder to analise -> " + str(num_folder))

    for el in res:
        logging.debug("Folder under analysis -> " + str(el))
        second_path = realpath + str(el) + "/scores/"
        # realpath = "/Users/alessandrozonta/Desktop/Experiment-testnewoutput/1/"
        files = 0
        names = []
        for i in os.listdir(second_path):
            if os.path.isfile(os.path.join(second_path, i)) and 'scores-' in i and ".zip" in i:
                files += 1
                names.append(i)

        names.sort()
        max = files
        vect = np.arange(1, max + 1)
        # print vect
        numb = 0
        for name in names:


            path = second_path + name

            try:
                with zipfile.ZipFile(path) as z:
                    with z.open(z.namelist()[0]) as f:
                        content = f.readlines()
                        pos = content[0].find("{")
                        content = content[0][pos:]
                        json_file = json.loads(content)

                        # for el in json_file["scores"]:
                        #     print el

                        v = []


                        for el in json_file["scores"]:
                            # vector = json.loads(el)
                            vect = el.split(",")
                            v.append((int(vect[0].replace("[", "")), int(vect[1]), int(float(vect[3].replace("]",""))), vect[2]))

                        # sort the list of tuples
                        v.sort(key=lambda tup: tup[0])

                        agent = []
                        classifier = []
                        result = []
                        for el in v:
                            # select only with the
                            agent.append(el[0])
                            classifier.append(el[1])
                            result.append(el[2])

                        # need to order per agent

                        classifier_array = np.array(classifier)
                        agent_array = np.array(agent)



                        min_cla = np.amin(classifier_array)
                        max_cla = np.amax(classifier_array)
                        unique_element_classifier = np.unique(classifier_array)
                        # print(unique_element_classifier)
                        # print(len(unique_element_classifier))
                        unique_element_agent = np.unique(agent_array)
                        # print(unique_element_agent)
                        # print(len(unique_element_agent))

                        dif_cla = max_cla - min_cla

                        real_classifier = np.zeros(len(unique_element_classifier))

                        # (maxEnd - minEnd) * ((value - minStart) / (maxStart - minStart)) + minEnd;

                        value_agent = agent[0]
                        clax = []

                        final = []
                        for i in range(len(agent) + 1):
                            if i >= len(agent):
                                # sort the list of tuples
                                clax.sort(key=lambda tup: tup[0])

                                real_result_ordered = []
                                for el in clax:
                                    real_result_ordered.append(el[1])

                                final.append(real_result_ordered)
                            else:
                                if agent[i] == value_agent:
                                    clax.append((classifier[i], result[i]))
                                else:
                                    value_agent = agent[i]

                                    # sort the list of tuples
                                    clax.sort(key=lambda tup: tup[0])

                                    real_result_ordered = []
                                    for el in clax:
                                        real_result_ordered.append(el[1])

                                    final.append(real_result_ordered)

                                    clax = []
                                    clax.append((classifier[i], result[i]))

                        df = DataFrame(data=final)

                        sns.set()

                        plt.figure(numb)
                        ax = sns.heatmap(df, vmin=0, vmax=1)
                        plt.xlabel("Classifiers")
                        plt.ylabel("Agents")

                        logging.debug("Generating frame " + str(numb))

                        fname = second_path + '_tmpscore%05d.png' % numb
                        plt.savefig(fname)
                        plt.clf()
                numb += 1
            except:
                pass

    # os.system("rm movie.mp4")
    # os.system("ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4")
    # os.system("rm _tmp*.png")
    # plt.show()
