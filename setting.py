import json
import logging
import os

import sys

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    print(sys.argv)

    with open('settings.json') as data_file:
        data = json.load(data_file)

    data["Experiment"] = str(numbExperiment)
    data["Name"] = str(Name)
    data["StepSizeAgents"] = float(StepSizeAgents)
    data["StepSizeClassifiers"] = float(StepSizeClassifiers)

    os.remove('settings.json')

    with open('settings.json', 'w') as outfile:
        json.dump(data, outfile)

    logging.debug("End Program")
