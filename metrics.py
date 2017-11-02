import logging
import matplotlib.pyplot as plt

from pandas import DataFrame, np

from HaasdijkGraph import analise


def print_statistics(total):
    real_total_list = []
    for el in total[0][1]:
        sub_total = []
        for subel in el:
            sub_total.append(float(subel.replace(",", "")))
        sub_total = np.sort(sub_total)
        real_total_list.append(sub_total)

    columns = []
    for i in range(0, 100):
        test = []
        columns.append(test)

    # el is a row
    for el in real_total_list:
        # all the element in the row are different columns
        for i in range(0, len(el)):
            columns[i].append(el[i])

    x = {}
    for i in range(0, len(columns)):
        x[i] = columns[i]

    dfs = DataFrame(data=x)
    standard_deviation = dfs.std(axis=1).values
    mean = dfs.mean(axis=1).values

    engagement = []
    for i in range(0, dfs.shape[0]):
        row = dfs.iloc[[i]]
        engagement.append(metric_disengagement(row, i))

    measure = []
    for i in range(len(standard_deviation)):
        measure.append({"std": standard_deviation[i], "mean": mean[i], "engagement": engagement[i]})

    return measure


def metric_disengagement(row, j):
    classes = []
    for i in range(row.size):
        if row[i][j] not in classes:
            classes.append(row[i][j])
    # count number of non empty classes
    c = len(classes)
    # not using C since I know for sure total number of classes is bigger than the populaiton size
    return (float)(c - 1) / (row.size - 1)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    total_agent, total_classifier = analise("/Users/alessandrozonta/Desktop/ex/res1")

    measurements = print_statistics(total_agent)

    for el in measurements:
        print el

    plt.figure(0)
    x = []
    e = []
    y = []
    count = 0
    for el in measurements:
        y.append(el["mean"])
        e.append(el["std"])
        x.append(count)
        count += 1

    plt.errorbar(x, y, e, linestyle='None', marker='^')

    plt.figure(1)
    y = []
    for el in measurements:
        y.append(el["engagement"])

    plt.plot(x, y, marker='^')

    plt.figure(2)
    y = []
    for el in measurements:
        y.append(el["std"])

    plt.plot(x, y, marker='^')

    plt.show()




    logging.debug("End Program")
