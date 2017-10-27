import os

comb = []
comb.append({"Experiment": 0, "Name": "Automation", "StepSizeAgents": 0.001, "StepSizeClassifiers": 0.001})
comb.append({"Experiment": 1, "Name": "Automation", "StepSizeAgents": 0.001, "StepSizeClassifiers": 0.01})
comb.append({"Experiment": 2, "Name": "Automation", "StepSizeAgents": 0.001, "StepSizeClassifiers": 0.1})
comb.append({"Experiment": 3, "Name": "Automation", "StepSizeAgents": 0.005, "StepSizeClassifiers": 0.01})
comb.append({"Experiment": 4, "Name": "Automation", "StepSizeAgents": 0.005, "StepSizeClassifiers": 0.1})


path = os.getcwd()
f = open(path + "/p0", 'a')
for element in comb:
    f.write(
        "{0} {1} {2} {3}\n".format(str(element["Experiment"]), str(element["Name"]), str(element["StepSizeAgents"]), str(element["StepSizeClassifiers"])))
f.close()
