import json
import logging
import matplotlib.pyplot as plt
import seaborn as sns

from pandas import DataFrame, np


def transform(value, max_old, min_old, max_new, min_new):
    return (max_new - min_new) * ((value - min_old) / (max_old - min_old)) + min_new


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-Test/2/scores-4-4.json"

    with open(path) as f:
        content = f.readlines()
        pos = content[0].find("{")
        content = content[0][pos:]
        json_file = json.loads(content)

        for el in json_file["scores"]:
            print el

        v = []

        for el in json_file["scores"]:
            vector = json.loads(el)
            v.append((int(vector[0]), int(vector[1]), int(vector[3])))

        # sort the list of tuples
        v.sort(key=lambda tup: tup[0])

        agent = []
        classifier = []
        result = []
        for el in v:
            # select only with the
            agent.append(el[0])
            classifier.append(el[1])
            result.append(el[2])

        # need to order per agent

        classifier_array = np.array(classifier)
        agent_array = np.array(agent)

        min_cla = np.amin(classifier_array)
        max_cla = np.amax(classifier_array)
        unique_element_classifier = np.unique(classifier_array)
        print unique_element_classifier
        unique_element_agent = np.unique(agent_array)
        print unique_element_agent
        dif_cla = max_cla - min_cla

        real_classifier = np.zeros(len(unique_element_classifier))

        # (maxEnd - minEnd) * ((value - minStart) / (maxStart - minStart)) + minEnd;

        value_agent = agent[0]
        clax = []

        final = []
        for i in range(len(agent) + 1):
            if i >= len(agent):
                # sort the list of tuples
                clax.sort(key=lambda tup: tup[0])

                real_result_ordered = []
                for el in clax:
                    real_result_ordered.append(el[1])

                final.append(real_result_ordered)
            else:
                if agent[i] == value_agent:
                    clax.append((classifier[i], result[i]))
                else:
                    value_agent = agent[i]

                    # sort the list of tuples
                    clax.sort(key=lambda tup: tup[0])

                    real_result_ordered = []
                    for el in clax:
                        real_result_ordered.append(el[1])

                    final.append(real_result_ordered)

                    clax = []
                    clax.append((classifier[i], result[i]))

        df = DataFrame(data=final)

        sns.set()

        ax = sns.heatmap(df)
        plt.xlabel("Classifiers")
        plt.ylabel("Agents")
        plt.show()
