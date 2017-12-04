import json
import logging
import time
import os

import sys

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    name = "FixedBearing"
    trajectoriesTrained = 20
    numb_exp = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    step_size_agent = [0.09, 0.1, 0.11, 0.09, 0.1, 0.11, 0.09, 0.1, 0.11]
    step_size_agent = [0.1, 0.1, 0.1, 0.11, 0.11, 0.11, 0.09, 0.09, 0.09]

    for i in range(len(numb_exp)):

        with open('settings.json') as data_file:
            data = json.load(data_file)

        data["Experiment"] = str(numb_exp[i])
        data["StepSizeAgents"] = float(step_size_agent[i])
        data["StepSizeClassifiers"] = float(step_size_agent[i])
        data["Name"] = str(name)
        data["TrajectoriesTrained"] = int(trajectoriesTrained)

        os.remove('settings.json')

        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)

        logging.debug("launch job ->" + str(numb_exp[i]))
        os.system("sbatch job")
        time.sleep(5)

    os.system("squeue")
    logging.debug("End Program")

