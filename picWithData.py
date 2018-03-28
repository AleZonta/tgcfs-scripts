import sys
import logging
import zipfile
import os
import json
from pandas import np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import tqdm
import subprocess
from visPointGenNoGoogle import *
from pandas import DataFrame


def plot_one_trajectory(trajectories_label, json_file, numb, max, real_total_min_lat, real_total_min_lng,
                        real_total_max_lat, real_total_max_lng, df):
    # real_total_min_lat = 52.045906899999999
    # real_total_min_lng = 4.331558
    # real_total_max_lat = 52.045942
    # real_total_max_lng = 4.3316090999999997
    # real_total_min_lat = 52.0422
    # real_total_min_lng = 4.31475
    # real_total_max_lat = 52.0427
    # real_total_max_lng = 4.3155

    # logging.debug("Computing graph " + str(numb))
    logging.debug("Info Trajectory")
    logging.debug(df.to_string())
    plt.figure(figsize=(10, 8))

    for ell in trajectories_label:
        printTrajectory(json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"],
                        real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng, plt,
                        json_file[ell]["classification"], max)

    plt.colorbar()
    plt.show()


def manyTrajectories(json_file, trajectories_label):
    total_list_different_trajectories = {}
    real_id_tra = []

    total_trajectories = []

    total_info_trajectories = []
    total_info_fitness = []

    count = 0

    for trajectory in trajectories_label:

        # transform trajectory in lat and lng
        lat_real = json_file[trajectory]["trajectory"][1][0]
        lng_real = json_file[trajectory]["trajectory"][1][1]

        key = str(lat_real) + str(lng_real)

        if key not in total_list_different_trajectories:
            total_list_different_trajectories.update({key: count})
            real_id_tra.append(json_file[trajectory]["id"])
            count += 1

            lat = []
            lng = []
            for el in json_file[trajectory]["trajectory"]:
                lat.append(el[0])
                lng.append(el[1])

            # transform real in lat and lng
            lat_real_h = []
            lng_real_h = []
            for el in json_file[trajectory]["real"]:
                lat_real_h.append(el[0])
                lng_real_h.append(el[1])

            total_trajectories.append(
                {"lats_tra": lat, "lng_tra": lng, "lats_real": lat_real_h, "lng_real": lng_real_h})

            # transform generated in lat and lng
            lat_generated = []
            lng_generated = []
            for el in json_file[trajectory]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])

            fit = json_file[trajectory]["classification"]

            vect_generated = []
            vect_generated.append((lat_generated, lng_generated))
            total_info_trajectories.append(vect_generated)
            vect_fitness = []
            vect_fitness.append(fit)
            total_info_fitness.append(vect_fitness)
        else:
            position = total_list_different_trajectories[key]

            # transform generated in lat and lng
            lat_generated = []
            lng_generated = []
            for el in json_file[trajectory]["generated"]:
                lat_generated.append(el[0])
                lng_generated.append(el[1])

            fit = json_file[trajectory]["classification"]

            total_info_trajectories[position].append((lat_generated, lng_generated))
            total_info_fitness[position].append(fit)

    plt.figure(figsize=(12, 10))
    plt.autoscale(enable=False, tight=True)

    sns.set_style("darkgrid")
    for i in range(len(total_trajectories)):
        j = i + 1
        # plt.subplot(3, 4, j)
        plt.subplot(3, 4, j)


        lats = total_trajectories[i]["lats_tra"]
        lngs = total_trajectories[i]["lng_tra"]

        lat_real = total_trajectories[i]["lats_real"]
        lng_real = total_trajectories[i]["lng_real"]

        lat_g = []
        lng_g = []
        for el in total_info_trajectories[i]:
            lat_g.append(el[0])
            lng_g.append(el[1])

        fitness = total_info_fitness[i]
        max = 150

        min_lat = []
        max_lat = []
        min_lng = []
        max_lng = []
        min_lat.append(np.amin(np.array(lat_g)))
        max_lat.append(np.amax(np.array(lat_g)))
        min_lng.append(np.amin(np.array(lng_g)))
        max_lng.append(np.amax(np.array(lng_g)))
        min_lat.append(np.amin(np.array(lats)))
        max_lat.append(np.amax(np.array(lats)))
        min_lng.append(np.amin(np.array(lngs)))
        max_lng.append(np.amax(np.array(lngs)))
        min_lat.append(np.amin(np.array(lat_real)))
        max_lat.append(np.amax(np.array(lat_real)))
        min_lng.append(np.amin(np.array(lng_real)))
        max_lng.append(np.amax(np.array(lng_real)))
        real_min_lat = np.amin(np.array(min_lat)) - 0.0002
        real_max_lat = np.amax(np.array(max_lat)) + 0.0002
        real_min_lng = np.amin(np.array(min_lng)) - 0.0002
        real_max_lng = np.amax(np.array(max_lng)) + 0.0002

        plt.axis([real_min_lat, real_max_lat, real_min_lng, real_max_lng])
        # plt.xlim(real_min_lat, real_max_lat)
        # plt.ylim(real_min_lng, real_max_lng)
        plt.axis('off')

        # trajectory
        plt.plot(lats, lngs, color='b', marker='o', markersize=1)

        # print real point
        plt.plot(lat_real, lng_real, color='k', marker='o', markersize=1)

        plt.scatter(lat_g, lng_g, c=[fitness], marker='o', vmin=0., vmax=max, cmap='cool', s=1)

        # print generated point
        # for k in range(len(lat_g)):
        #     plt.plot(lat_g[k], lng_g[k], color='r', marker='o', markersize=1)

    plt.show()
    plt.close()


def find_data_generation(selected_pic, path):
    path += "/classifier.log"

    with open(path) as f:
        content = f.readlines()

        interesting_list = []
        for el in content:
            # if "evaluateIndividuals {" in el:
            if "INFO: {" in el:
                interesting_list.append(el)

        interesting_list = interesting_list[selected_pic]
        # interesting_list = interesting_list[63:]
        interesting_list = interesting_list[6:]

        first_closing = interesting_list.find("}}") + len("}}")

        classifiers = []
        classifier = interesting_list[1:first_closing]
        classifiers.append(classifier)
        while len(interesting_list) > 10:
            interesting_list = interesting_list[first_closing:]
            first_closing = interesting_list.find("}}") + len("}}")
            if first_closing is not None:
                classifier = interesting_list[:first_closing]
                classifiers.append(classifier[2:])

        classifiers = classifiers[:-1]
        gen = 0
        df = DataFrame(columns=['classifier', 'agent', 'trajectory', 'value'])
        for clax in classifiers:
            first_equals = clax.find("=")
            number = clax[:first_equals]
            clax = clax[first_equals + 2:-1]

            parts = clax.split("},")

            for agent in parts:
                agent = agent.strip()
                first_equals = clax.find("=")
                numberAgent = agent[:first_equals]
                plus_smth = 2
                if "=" in numberAgent:
                    numberAgent = numberAgent[:-1]
                    plus_smth = 1
                res = agent[first_equals + plus_smth:-1]

                sub_res = res.split(',')
                for res in sub_res:
                    parts = res.split("=")

                    d = {"classifier": int(number), "agent": int(numberAgent), "trajectory": parts[0],
                         "value": float(parts[1])}
                    dfs = DataFrame(data=d, index=[gen])
                    gen += 1
                    df = df.append(dfs)

        return df


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # try:
    #     first_path = sys.argv[1]
    # except Exception as e:
    #     logging.debug("path, max_agent and max_classifier not passed. Program not going to work")
    #     sys.exit()

    first_path = "/Users/alessandrozonta/Desktop/"

    folders = how_many_fatherFolder(first_path)

    folders = ["Experiment-test"]

    one_or_more = 0

    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)

        res = ["000"]

        selected_pic = 20

        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            path = second_path + str(el) + "/"

            # check max fitness achiavable
            maxx = find_max_fitnes(path)

            names = []
            for i in os.listdir(path):
                name_to_check = "trajectory-generatedPoints-"
                # if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                if os.path.isfile(os.path.join(path, i)) and name_to_check in i and ".zip" in i:
                    names.append(i)

            names = sorted_nicely(names)

            names = names[selected_pic]

            min_lat = 0
            min_lng = 0
            max_lat = 0
            max_lng = 0
            if one_or_more == 1:
                logging.debug("Finding boundaries...")
                # checking only 1/4 of all the trajectory in order to find the boudaries

                total_checked_folder = len(names) / 4

                list_different_tra = {}
                max_min_info = []

                trajectories_label, json_file = reanInfo(path + names)

                total_min_lat = []
                total_min_lng = []
                total_max_lat = []
                total_max_lng = []
                for ell in trajectories_label:
                    real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng = find_max_min_coordinates(
                        json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"])
                    total_min_lat.append(real_total_min_lat)
                    total_min_lng.append(real_total_min_lng)
                    total_max_lat.append(real_total_max_lat)
                    total_max_lng.append(real_total_max_lng)

                min_lat = np.amin(np.array(total_min_lat)) - 0.0001
                min_lng = np.amin(np.array(total_min_lng)) - 0.0001
                max_lat = np.amax(np.array(total_max_lat)) + 0.0001
                max_lng = np.amax(np.array(total_max_lng)) + 0.0001

                logging.debug("Boundaries found!")

            df = find_data_generation(selected_pic, path)


            logging.debug("Creating graphs...")
            name = names
            # name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"
            # numb = int(name.replace("trajectory-generatedPoints-", "").replace(".zip", "").split("-")[0])
            name_to_check = "trajectory-generatedPoints-"
            numb = int(name.replace(name_to_check, "").replace(".zip", "").split("-")[0])
            # logging.debug("Analysing " + str(path) + str(name))
            trajectories_label, json_file = reanInfo(path + name)

            if one_or_more == 1:
                plot_one_trajectory(trajectories_label, json_file, numb, maxx, min_lat, min_lng, max_lat, max_lng, df)
            else:
                groups_df = df.groupby("trajectory").groups.keys()
                for g in groups_df:
                    logging.debug(df.loc[df['trajectory'] == g].to_string())

                manyTrajectories(json_file, trajectories_label)



            # else:
            #     logging.debug("Pictures already present in the folder")
            logging.debug("Graphs created!")

            # bashCommand = "ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4"
            # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=path)
            # output, error = process.communicate()
            #
            # logging.debug("Video created!")

    logging.debug("End Program")
