import logging
import csv
from pandas import DataFrame
import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.debug("Starting Elaboration")

    first_path = "/Volumes/TheMaze/TuringLearning/february/snow/Experiment-plusplusGeolife10/5"
    path = first_path + "/statistic.csv"

    with open(path, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)


        different_trajectories = []
        for generation in your_list:


            # find if trajectories

            generation = generation[:-1]

            for trajectory in generation:
                first_pos = trajectory.index("Trajectory:") + len("Trajectory:")
                end_pos = trajectory.index("DistanceBetweenPoints")
                tra = trajectory[first_pos:-(len(trajectory) - end_pos)].strip()
                if tra not in different_trajectories:
                    different_trajectories.append(tra)

        df = DataFrame(columns=['gen', 'tra', 'distance', 'difference', 'combination'])
        # found the total number of trajectories
        for i in tqdm.tqdm(range(len(your_list))):
            generation = your_list[i]
            generation = generation[:-1]
            for trajectory in generation:
                first_pos = trajectory.index("Trajectory:") + len("Trajectory:")
                end_pos = trajectory.index("DistanceBetweenPoints")

                tra = trajectory[first_pos:-(len(trajectory) - end_pos)].strip()

                first_pos = trajectory.index("DistanceBetweenPoints:") + len("DistanceBetweenPoints:")
                end_pos = trajectory.index(";")
                first_pos_bearing = trajectory.index("DifferenceInBearing:") + len("DifferenceInBearing:")
                end_pos_bearing = trajectory.index("}")

                distance = float(trajectory[first_pos:-(len(trajectory) - end_pos)].strip())
                difference = float(trajectory[first_pos_bearing:-(len(trajectory) - end_pos_bearing)].strip())

                index_trajectory = different_trajectories.index(tra)

                combined_valued = distance * 100 + difference

                d = {"gen": i, "tra": index_trajectory, "distance": distance, "difference": difference, "combination": combined_valued}
                dfs = DataFrame(data=d, index=[i])
                df = df.append(dfs)

        df = df[df.columns].astype(float)
        logging.debug("Dataframe Generated")
        # df.to_csv("dataframe.csv")

        sns.set(style="ticks")

        sns.regplot(x="gen", y="combination", data=df)
        plt.show()