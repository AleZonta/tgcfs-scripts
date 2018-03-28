import logging
from fitnessAngleDistance import analise_distances
from pandas import np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
import statsmodels.api as sm


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    # first_path = "/Volumes/TheMaze/TuringLearning/february/15feb/Experiment-plusplusGeolife/"
    first_path = "/Volumes/TheMaze/TuringLearning/february/snow/Experiment-plusplus/"

    # read all the trajectories for the distance to the real point
    logging.debug("Checking the distances...")
    real_distances, real_distances_bearing = analise_distances(first_path, "0/", True)
    # 0 np.max(array), 1 np.min(array), 2 np.mean(array), 3 np.std(array), 4 np.median(array)

    # single graphs
    trajectories = len(real_distances[0].keys())
    num = np.arange(0, trajectories)
    real_total = []
    number_tra = []
    for tra in range(trajectories):
        x = []
        x = np.arange(0, len(real_distances))
        median = []
        for el in real_distances:
            median.append(np.median(np.array(el[tra][1])))

        median_bearing = []
        for el in real_distances_bearing:
            median_bearing.append(np.median(np.array(el[tra][1])))

        total_sum_median = []
        for i in range(len(median)):
            total_sum_median.append(median[i] * 100 + median_bearing[i])

        for el in total_sum_median:
            real_total.append(el)
            number_tra.append(tra)

    # x = np.arange(0, len(real_distances))
    # total_x = []
    # for i in range(trajectories):
    #     for el in x:
    #         total_x.append(el)
    #
    # zz = {"Generations": total_x, "Medians": real_total, "Trajectory": number_tra}
    # dfs = DataFrame(data=zz)
    # sns.set_style("darkgrid")
    # sns.set(rc={'figure.figsize': (12, 6)})
    # sns.lmplot("Generations", "Medians", data=dfs, hue="Trajectory")
    # sns.despine()

    #pic with all together

    x = []
    x = np.arange(0, len(real_distances))
    median = []
    for el in real_distances:
        a = []
        for k in el.keys():
            a.append(el[k][1])
        median.append(np.median(np.array(a)))

    median_bearing = []
    for el in real_distances_bearing:
        a = []
        for k in el.keys():
            a.append(el[k][1])
        median_bearing.append(np.median(np.array(a)))

    total_sum_median = []
    for i in range(len(median)):
        total_sum_median.append(median[i] * 100 + median_bearing[i])

    zz = {"Generations": x, "Medians": total_sum_median}
    dfs = DataFrame(data=zz)
    sns.set_style("darkgrid")
    sns.set(rc={'figure.figsize': (12, 6)})
    sns.lmplot("Generations", "Medians", data=dfs )
    sns.despine()

    # linear regression
    X = dfs["Generations"]
    y = dfs["Medians"]

    # Note the difference in argument order
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)  # make the predictions by the model

    # Print out the statistics
    logging.debug(model.summary())

    # fit = np.polyfit(x, total_sum_median, 1)
    # fit_fn = np.poly1d(fit)

    # plt.figure(trajectories + 1, figsize=(12, 6))
    # sns.set_style("darkgrid")
    #
    # plt.plot(x, total_sum_median, 'yo', x, fit_fn(x), '--k')
    # plt.xlabel("Generation")

    plt.show()
