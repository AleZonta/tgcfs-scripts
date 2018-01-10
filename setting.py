import json
import logging
import os

import sys

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # print(sys.argv)
    # name = sys.argv[1]
    # numbExperiment = sys.argv[2]
    # StepSizeAgents = sys.argv[2]
    # StepSizeClassifiers = sys.argv[3]
    # TournamentSizeClassifiers = sys.argv[5]
    # DifferentSelectionForClassifiers = sys.argv[3]
    # OffspringSizeAgent = sys.argv[4]
    # OffspringSizeClassifier = sys.argv[5]
    # KeepBestNElement = sys.argv[6]

    name = "Test"

    with open('settings.json') as data_file:
        data = json.load(data_file)

    data["Name"] = str(name)
    # data["Experiment"] = str(numbExperiment)
    # data["StepSizeAgents"] = float(StepSizeAgents)
    # data["StepSizeClassifiers"] = float(StepSizeClassifiers)
    # data["TournamentSizeClassifiers"] = int(TournamentSizeClassifiers)
    # data["DifferentSelectionForClassifiers"] = float(DifferentSelectionForClassifiers)
    # data["AgentOffspringSize"] = int(OffspringSizeAgent)
    # data["ClassifierOffspringSize"] = int(OffspringSizeClassifier)
    # data["KeepBestNElement"] = int(KeepBestNElement)
    data["UsingReducedVirulenceMethodOnClassifiers"] = True


    os.remove('settings.json')

    with open('settings.json', 'w') as outfile:
        json.dump(data, outfile)

    logging.debug("End Program")
