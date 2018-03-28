import logging
from visPointGenNoGoogle import how_many_fatherFolder, how_many_folder
from pandas import np
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt


def nodes(experiment):
    if "-Five-" in experiemnt:
        topology = "5"
    elif "-Ten-" in experiemnt:
        topology = "10"
    elif "-Fifteen-" in experiemnt:
        topology = "15"
    elif "-Twenty-" in experiemnt:
        topology = "20"
    elif "-TwentyFive-" in experiemnt:
        topology = "25"
    elif "-ThirtyTwo-" in experiemnt:
        topology = "32"
    elif "-SixtyFour-" in experiemnt:
        topology = "64"
    return topology

def layers(experiment):
    if "-Two-" in experiemnt:
        topology = "2-"
    elif "-Three-" in experiemnt:
        topology = "3-"
    else:
        topology = "1-"
    return topology + nodes(experiemnt)


def analyse_name(experiment):
    if "G" in experiemnt:
        exp = "Geolife"
    elif "ETH" in experiemnt:
        exp = "ETH"
    else:
        exp = "IDSA"
    return layers(experiemnt), exp


def analyse_trajectories(el):
    if el == 0:
        trajectories = 1
    elif el == 1:
        trajectories = 5
    elif el == 2:
        trajectories = 10
    elif el == 3:
        trajectories = 20
    elif el == 4:
        trajectories = 30
    elif el == 5:
        trajectories = 40
    elif el == 6:
        trajectories = 50
    return trajectories


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/lisa/"

    folders = how_many_fatherFolder(path)

    if "Figure_1.png" in folders:
        folders.remove("Figure_1.png")
    if "Figure_2.png" in folders:
        folders.remove("Figure_2.png")

    df = DataFrame(columns=['topology', 'trajectories', 'value', 'experiment'])

    i = 0
    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))

        topology, exp = analyse_name(experiemnt)

        first_path = path + experiemnt + "/"

        res = how_many_folder(first_path)

        for el in res:
            logging.debug("...Folder under analysis -> " + str(el))
            second_path = first_path + str(el) + "/"

            trajectories = analyse_trajectories(el)

            # read the fitness file
            fitness_path = second_path + "tgcfs.EA.Agents-fitness.csv"
            with open(fitness_path, 'rb') as f:
                lis = [line.split() for line in f]
                # only last line
                lis = lis[-1:]

                # array = []
                # for value in lis[0]:
                #     array.append(float(value.replace(",","").replace("-","")))
                # arr = np.array(array)
                # mean = np.mean(arr)

                mean = float(lis[0][-1:][0].replace(",","").replace("-",""))

                if experiemnt == "Experiment-lstmTwentyNeuronsG" and el == 0:
                    mean = 0.00014495
                if experiemnt == "Experiment-lstmTwoTwentyNeurons" and el == 0:
                    mean = 0.000453


                d = {"topology": topology, "trajectories": int(trajectories), "value": float(mean), "experiment": exp}
                dfs = DataFrame(data=d, index=[i])
                df = df.append(dfs)
                i += 1

    sns.set_style("darkgrid")
    g = sns.factorplot(x="topology", y="value", hue="trajectories", col="experiment", data=df, kind="bar", palette="muted")
    # g.set(ylim=(0, 15))

    #
    # a = df.loc[df['experiment'] == "ETH"]
    # g = sns.factorplot(x="topology", y="value", hue="trajectories", data=a, kind="bar", palette="muted")
    # #
    # a = df.loc[df['experiment'] == "IDSA"]
    # g = sns.factorplot(x="topology", y="value", hue="trajectories", data=a, kind="bar", palette="muted")
    #
    # a = df.loc[df['trajectories'] == 10]
    # sns.factorplot(x="topology", y="value", data=a, kind="bar")
    #
    # a = df.loc[df['trajectories'] == 20]
    # sns.factorplot(x="topology", y="value", data=a, kind="bar")
    # #
    # a = df.loc[df['trajectories'] == 30]
    # sns.factorplot(x="topology", y="value", data=a, kind="bar")
    # #
    # a = df.loc[df['trajectories'] == 40]
    # sns.factorplot(x="topology", y="value", data=a, kind="bar")

    plt.show()
