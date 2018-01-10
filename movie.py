import logging
from fitnessAngleDistance import how_many_folder
import subprocess
import os
import fnmatch


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Volumes/TheMaze/TuringLearning/Experiment Christmas Holidays/Experiment-200keeptop10"
    folders = how_many_folder(path)
    num_folder = len(folders)
    logging.debug("Folder to analise -> " + str(num_folder))

    for folder in folders:
        logging.debug("Analysing folder " + str(folder))

        real_path = path + "/" + str(folder) + "/pic/"

        if os.path.exists(real_path + "_tmp00013.png"):

            # count number of png
            number_of_png = len(fnmatch.filter(os.listdir(real_path), '*.png'))
            logging.debug("Number of png -> " + str(number_of_png))

            if number_of_png > 900:

                if not os.path.exists(real_path + "movie.mp4"):

                    bashCommand = "ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4"
                    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd=real_path)
                    output, error = process.communicate()
                else:
                    logging.debug("Video already present")
            else:
                logging.debug("Not all the pic are available to generate the movie")

        else:
            logging.debug("No pictures found to create the movie")