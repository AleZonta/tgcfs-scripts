import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-cccc/0/classifier.log"

    with open(path) as f:
        content = f.readlines()

        output = []
        transormed = []
        for el in content:
            if "runLSTM Output LSTM ->" in el:
                output.append(el[-15:].replace("\n", "").replace("[", "").replace("]", "").replace(">", "").split(","))
            if "runLSTM Output LSTM transformed" in el:
                transormed.append(
                    el[-60:].replace("r", "").replace("r", "").replace("k", "").replace("t", "").replace("s",
                                                                                                         "").replace(
                        "p", "").replace("d", "").replace("=", "").replace("N", "").replace("e", "").replace("w",
                                                                                                             "").replace(
                        "o", "").replace("{", "").replace("}", "").replace("g", "").replace("b", "").replace("a", "").replace("i", "").replace("n", "").replace("]", "").replace("speed=", "").replace(
                        "beaing=", "")[:-3].split(","))

        firstOutput = []
        firstTransformed = []
        for i in range(len(output)):
            firstOutput.append(float(output[i][0]))
            firstTransformed.append(float(format(float(transormed[i][0]), '.2f')))

        firstOutputDict = {}
        for el in firstOutput:
            if el in firstOutputDict:
                firstOutputDict[el] += 1
            else:
                firstOutputDict.update({el: 0})

        firstOutputTransormedDict = {}
        for el in firstTransformed:
            if el in firstOutputTransormedDict:
                firstOutputTransormedDict[el] += 1
            else:
                firstOutputTransormedDict.update({el: 0})

        tips = pd.DataFrame(firstOutputDict.items(), columns=['Value', 'Occurrences'])

        plt.figure(0)
        sns.set_style("whitegrid")
        ax = sns.barplot(x="Value", y="Occurrences", data=tips)

        tipsTransformed = pd.DataFrame(firstOutputTransormedDict.items(), columns=['Value', 'Occurrences'])

        plt.figure(1)
        sns.set_style("whitegrid")
        ax = sns.barplot(x="Value", y="Occurrences", data=tipsTransformed)


        firstOutput = []
        firstTransformed = []
        for i in range(len(output)):
            firstOutput.append(float(output[i][1]))
            firstTransformed.append(float(format(float(transormed[i][1]), '.2f')))

        firstOutputDict = {}
        for el in firstOutput:
            if el in firstOutputDict:
                firstOutputDict[el] += 1
            else:
                firstOutputDict.update({el: 0})

        firstOutputTransormedDict = {}
        for el in firstTransformed:
            if el in firstOutputTransormedDict:
                firstOutputTransormedDict[el] += 1
            else:
                firstOutputTransormedDict.update({el: 0})

        tipsOu = pd.DataFrame(firstOutputDict.items(), columns=['Value', 'Occurrences'])

        plt.figure(2)
        sns.set_style("whitegrid")
        ax = sns.barplot(x="Value", y="Occurrences", data=tipsOu)

        tipsTransformedOu = pd.DataFrame(firstOutputTransormedDict.items(), columns=['Value', 'Occurrences'])

        plt.figure(3)
        sns.set_style("whitegrid")
        ax = sns.barplot(x="Value", y="Occurrences", data=tipsTransformedOu)

        plt.show()
        asd = ""
