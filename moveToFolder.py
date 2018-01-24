import logging
from fitnessAngleDistance import how_many_folder
from visPointGenNoGoogle import how_many_fatherFolder
import os
import glob
import shutil

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    first_path = "/Volumes/TheMaze/TuringLearning/january/latest/linear/"

    folders = how_many_fatherFolder(first_path)

    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))

        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)

        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            third_path = second_path + str(el) + "/"

            directory = third_path + "pic"
            try:
                os.stat(directory)
                shutil.rmtree(directory)
                os.mkdir(directory)
            except:
                os.mkdir(directory)

            count = 0
            for pngFile in glob.iglob(os.path.join(third_path, "*.png")):
                if "graph" not in pngFile:
                    count += 1
                    shutil.move(pngFile, directory)
            logging.debug("folder " + str(el) + " moved " + str(count) + " pic")

            fourth_path = third_path + "scores-12-12.zip"
            if os.path.exists(fourth_path):
                directory = third_path + "scores"
                try:
                    os.stat(directory)
                except:
                    os.mkdir(directory)

                count = 0
                for zipFile in glob.iglob(os.path.join(third_path, "*.zip")):
                    if "scores" in zipFile:
                        count += 1
                        shutil.move(zipFile, directory)
                logging.debug("folder " + str(el) + " moved " + str(count) + " scores")