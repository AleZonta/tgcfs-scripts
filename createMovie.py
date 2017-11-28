import logging

import gmplot
import json
import zipfile
from pandas import np
import imgkit
from selenium import webdriver
import time
import os
import os.path

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    num = [4]
    for el in num:

        path = "/Volumes/TheMaze/TuringLearning/SIKS/" + str(el) + "/"
        files = 0
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)) and 'trajectory-generatedPoints-' in i and ".zip" in i:
                files += 1

        max = files
        vect = np.arange(1, max + 1 )


        for numb in vect:
            name = "trajectory-generatedPoints-" + str(numb) + "-" + str(numb) + ".html"

        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # it requires this command to work
        # selenium-server -port 4444
        # on console of course
        # --------------------------------------------------------------
        # --------------------------------------------------------------

            save_name = '_tmp%05d.png' % numb
            if not os.path.exists(path + save_name):

                driver = webdriver.Chrome()
                driver.get("file://" + path + name)
        #
                time.sleep(2)
        #
                time.sleep(2)
        #
                driver.save_screenshot(path + save_name)
                driver.quit()
            else:
                logging.debug("File already exists " + str(numb))

    #os.system("rm movie.mp4")
    #os.system("ffmpeg -f image2 -r 2 -i _tmp%05d.png -vcodec mpeg4 -y movie.mp4")
    # os.system("rm _tmp*.png")
    logging.debug("End Program")
