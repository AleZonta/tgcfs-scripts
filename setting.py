import json
import logging
import os

import sys

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    print(sys.argv)
    numbExperiment = sys.argv[1]
    StepSizeAgents = sys.argv[2]
    StepSizeClassifiers = sys.argv[3]
    TournamentSizeClassifiers = sys.argv[5]
    DifferentSelectionForClassifiers = sys.argv[5]

    with open('settings.json') as data_file:
        data = json.load(data_file)

    data["Experiment"] = str(numbExperiment)
    data["StepSizeAgents"] = float(StepSizeAgents)
    data["StepSizeClassifiers"] = float(StepSizeClassifiers)
    data["TournamentSizeClassifiers"] = int(TournamentSizeClassifiers)
    data["DifferentSelectionForClassifiers"] = int(DifferentSelectionForClassifiers)


    os.remove('settings.json')

    with open('settings.json', 'w') as outfile:
        json.dump(data, outfile)

    logging.debug("End Program")
