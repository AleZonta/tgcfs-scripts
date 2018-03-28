from visPointGenNoGoogle import how_many_fatherFolder, how_many_folder
import logging
import os


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Volumes/TheMaze/TuringLearning/march/singleLSTM/"

    folders = how_many_fatherFolder(path)

    if "Figure_1.png" in folders:
        folders.remove("Figure_1.png")
    if "Figure_2.png" in folders:
        folders.remove("Figure_2.png")


    i = 0
    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))

        first_path = path + experiemnt + "/"

        res = how_many_folder(first_path)

        missing = []
        if len(res) != 5:
            if 3 not in res:
                missing.append(3)
            if 4 not in res:
                missing.append(4)
            if 5 not in res:
                missing.append(5)
            if 6 not in res:
                missing.append(6)
        if len(missing) > 0:
            logging.debug("...............Folder missing -> " + str(missing))

        for el in res:
            logging.debug("...Folder under analysis -> " + str(el))
            second_path = first_path + str(el) + "/"
            names = []
            for i in os.listdir(second_path):
                name_to_check = "trajectory-generate-aSs-"

                # if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                if os.path.isfile(os.path.join(second_path, i)) and name_to_check in i and ".zip" in i:
                    names.append(i)

            if len(names) < 4000:
                logging.debug("... missing files -> " + str(len(names)))