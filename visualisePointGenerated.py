import logging

import gmplot
import json
import zipfile
from pandas import np



def reanInfo(path):
    logging.debug("reading ZIP file")
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


def printMap():
    # center lat, center lng, zoom
    gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

    lat = [37.428]
    lng = [-122.145]
    # gmap.plot(lat, lng, 'cornflowerblue', edge_width=10)
    gmap.scatter(lat, lng, '#3B0B39', size=40, marker=False)
    # gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)

    gmap.draw("mymap.html")


def printTrajectory(gmap, real, generated, trajectory):
    logging.debug("converting JSON list to list for the library")
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

    logging.debug("plotting points")

    # print trajectory
    gmap.scatter(lat, lng, '#2b1aad', size=5, marker=False)

    # print real point
    gmap.scatter(lat_real, lng_real, '#1ccc42', size=5, marker=False)

    # print generated point
    gmap.scatter(lat_generated, lng_generated, '#cc1b1b', size=1, marker=False)

    # connect real point with generated
    lat_connection = []
    lng_connection = []
    lat_connection.append(lat_real[len(lat_real) - 1])
    lng_connection.append(lng_real[len(lng_real) - 1])
    lat_connection.append(lat_generated[0])
    lng_connection.append(lng_generated[0])

    gmap.plot(lat_connection, lng_connection, 'cornflowerblue', edge_width=10)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    max = 4
    vect = np.arange(1, max +1)
    for numb in vect:
        name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".zip"
        path = "/Users/alessandrozonta/Desktop/Experiment-Test/2/"
        trajectories_label, json_file = reanInfo(path + name)

        # lets try the first one
        print "----------------- first one -----------------"
        print json_file[trajectories_label[0]]["real"]
        print json_file[trajectories_label[0]]["generated"]
        print json_file[trajectories_label[0]]["trajectory"]
        # lets try the second one
        print "----------------- second one -----------------"
        print json_file[trajectories_label[1]]["real"]
        print json_file[trajectories_label[1]]["generated"]
        print json_file[trajectories_label[1]]["trajectory"]
        # lets try the third one
        print "----------------- third one -----------------"
        print json_file[trajectories_label[2]]["real"]
        print json_file[trajectories_label[2]]["generated"]
        print json_file[trajectories_label[2]]["trajectory"]
        #
        # # transform trajectory in lat and lng
        # lat = []
        # lng = []
        # for el in json_file[trajectories_label[0]]["trajectory"]:
        #     lat.append(el[0])
        #     lng.append(el[1])

        # center lat, center lng, zoom
        lat_real = []
        lng_real = []
        for el in json_file[trajectories_label[0]]["real"]:
            lat_real.append(el[0])
            lng_real.append(el[1])

        gmap = gmplot.GoogleMapPlotter(lat_real[0], lng_real[0], 16)

        for el in trajectories_label:
            printTrajectory(gmap, json_file[el]["real"], json_file[el]["generated"], json_file[el]["trajectory"])

        logging.debug("generating map")
        name = name[:-4]
        name += "html"
        gmap.draw(path + name)

    logging.debug("End Program")
