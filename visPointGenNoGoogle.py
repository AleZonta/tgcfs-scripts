import logging
import zipfile
import os
import json
from pandas import np
import matplotlib.pyplot as plt
import seaborn as sns



def reanInfo(path):
    # logging.debug("reading ZIP file")
    with zipfile.ZipFile(path) as z:
        with z.open(z.namelist()[0]) as f:
            content = f.readlines()
            content = content[0].replace("(", "[").replace(")", "]")
            pos = content.find("{")
            content = content[pos:]
            json_file = json.loads(content)

            trajectories_label = []
            for el in json_file:
                if "size" not in el:
                    trajectories_label.append(el)

            return trajectories_label, json_file


def printTrajectory(real, generated, trajectory, real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng, plt):
    # logging.debug("converting JSON list to list for the library")
    # transform trajectory in lat and lng
    lat = []
    lng = []
    for el in trajectory:
        lat.append(el[0])
        lng.append(el[1])

    # transform real in lat and lng
    lat_real = []
    lng_real = []
    for el in real:
        lat_real.append(el[0])
        lng_real.append(el[1])

    # transform generated in lat and lng
    lat_generated = []
    lng_generated = []
    for el in generated:
        lat_generated.append(el[0])
        lng_generated.append(el[1])

    sns.set_style("darkgrid")

    plt.axis([real_total_min_lat, real_total_max_lat, real_total_min_lng, real_total_max_lng])

    # print trajectory
    plt.plot(lat, lng, color='b', marker='o')

    # print real point
    plt.plot(lat_real, lng_real, color='g', marker='o')

    # print generated point
    for i in range(len(lat_generated)):
        plt.plot(lat_generated[i], lng_generated[i], color='r', marker='o')



def find_max_min_coordinates(real, generated, trajectory):
    # logging.debug("converting JSON list to list for the library")
    # transform trajectory in lat and lng
    lat = []
    lng = []
    for el in trajectory:
        lat.append(el[0])
        lng.append(el[1])

    # transform real in lat and lng
    lat_real = []
    lng_real = []
    for el in real:
        lat_real.append(el[0])
        lng_real.append(el[1])

    # transform generated in lat and lng
    lat_generated = []
    lng_generated = []
    for el in generated:
        lat_generated.append(el[0])
        lng_generated.append(el[1])

    # logging.debug("plotting points")
    min_lat = []
    min_lat.append(np.amin(np.array(lat)))
    min_lat.append(np.amin(np.array(lat_real)))
    min_lat.append(np.amin(np.array(lat_generated)))
    real_total_min_lat = np.amin(np.array(min_lat))

    min_lon = []
    min_lon.append(np.amin(np.array(lng)))
    min_lon.append(np.amin(np.array(lng_real)))
    min_lon.append(np.amin(np.array(lng_generated)))
    real_total_min_lng = np.amin(np.array(min_lon))

    max_lat = []
    max_lat.append(np.amax(np.array(lat)))
    max_lat.append(np.amax(np.array(lat_real)))
    max_lat.append(np.amax(np.array(lat_generated)))
    real_total_max_lat = np.amax(np.array(max_lat))

    max_lon = []
    max_lon.append(np.amax(np.array(lng)))
    max_lon.append(np.amax(np.array(lng_real)))
    max_lon.append(np.amax(np.array(lng_generated)))
    real_total_max_lng = np.amax(np.array((max_lon)))

    return real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    num = [0]
    for el in num:
        path = "/Users/alessandrozonta/Desktop/Das5/" + str(el) + "/"
        files = 0
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                files += 1

        max = files
        logging.debug("Files found " + str(max))
        vect = np.arange(1, max +1)
        for numb in vect:
            name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"
            logging.debug("Analysing " + str(path) + str(name))
            trajectories_label, json_file = reanInfo(path + name)

            logging.debug("Computing boundaries")
            min_lat = []
            min_lng = []
            max_lat = []
            max_lng = []
            for el in trajectories_label:
                real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng = find_max_min_coordinates(json_file[el]["real"], json_file[el]["generated"], json_file[el]["trajectory"])
                min_lat.append(real_total_min_lat)
                min_lng.append(real_total_min_lng)
                max_lat.append(real_total_max_lat)
                max_lng.append(real_total_max_lng)

            real_total_min_lat = np.amin(np.array(min_lat)) - 0.000005
            real_total_min_lng = np.amin(np.array(min_lng)) - 0.000005
            real_total_max_lat = np.amax(np.array(max_lat)) + 0.000005
            real_total_max_lng = np.amax(np.array(max_lng)) + 0.000005

            logging.debug("Computing graph " + str(numb))

            plt.figure(numb)

            for ell in trajectories_label:
                printTrajectory(json_file[ell]["real"], json_file[ell]["generated"], json_file[ell]["trajectory"], real_total_min_lat, real_total_min_lng, real_total_max_lat, real_total_max_lng, plt)

            save_name = path + '_tmp%05d.png' % numb
            plt.savefig(save_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)




    logging.debug("End Program")
