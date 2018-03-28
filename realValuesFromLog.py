import logging
from visPointGenNoGoogle import how_many_fatherFolder, how_many_folder
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import tqdm


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


    first_path = "/Users/alessandrozonta/Desktop/t/"

    folders = how_many_fatherFolder(first_path)

    folders = ["Experiment-cc"]

    for experiemnt in folders:
        logging.debug("Folder under analysis -> " + str(experiemnt))
        second_path = first_path + experiemnt + "/"
        res = how_many_folder(second_path)


        num_folder = len(res)
        logging.debug("Folder to analise -> " + str(num_folder))

        for el in res:
            path = second_path + str(el) + "/classifier.log"

            with open(path) as f:
                content = f.readlines()

                real_point_line = []
                interesting_list = []
                for el in content:
                    if "Output LSTM transformed" in el:
                        if "ut LSTM ->" not in el:
                            interesting_list.append(el)
                    if "Evaluation agent generation" in el:
                        interesting_list.append(el)
                    if "Real point transformed" in el:
                        real_point_line.append(el)

                different_tra = []
                for el in interesting_list:
                    if "Evaluation agent generation" in el:
                        if len(different_tra) > 0:
                            break
                    else:
                        try:
                            word = "tgcfs.EA.Agents$1ComputeUnit runLSTM"
                            pos_start = el.index(word) + len(word)
                            pop_end = el.index("Output LSTM transformed")
                        except Exception:
                            word = "INFO:"
                            pos_start = el.index(word) + len(word)
                            pop_end = el.index("Output LSTM transformed")

                        tra = el[pos_start:-(len(el) - pop_end)].strip()
                        if tra not in different_tra:
                            different_tra.append(tra)


                real_points_speed = []
                real_points_bearing = []
                for el in real_point_line:
                    pos_speed = el.index("speed=") + len("speed=")
                    pos_comma = el.index(",")
                    pos_bearing = el.index("bearing=") + len("bearing=")

                    speed = float(el[pos_speed:-(len(el) - pos_comma)].strip())
                    bearing = float(el[pos_bearing:-5].strip())

                    if speed not in real_points_speed:
                        real_points_speed.append(speed)
                    if bearing not in real_points_bearing:
                        real_points_bearing.append(bearing)

                df = DataFrame(columns=['gen','tra','speed','bearing'])
                gen = -1
                for i in tqdm.tqdm(range(len(interesting_list))):
                    el = interesting_list[i]
                    if "Evaluation agent generation" in el:
                        gen += 1
                    else:
                        try:
                            word = "tgcfs.EA.Agents$1ComputeUnit runLSTM"
                            pos_start = el.index(word) + len(word)
                            pop_end = el.index("Output LSTM transformed")
                        except Exception:
                            word = "INFO:"
                            pos_start = el.index(word) + len(word)
                            pop_end = el.index("Output LSTM transformed")

                        pos_speed = el.index("speed=") + len("speed=")
                        pos_comma = el.index(",")
                        pos_bearing = el.index("bearing=") + len("bearing=")

                        tra = el[pos_start:-(len(el) - pop_end)].strip()
                        speed = el[pos_speed:-(len(el) - pos_comma)].strip()
                        bearing = el[pos_bearing:-5].strip()

                        # logging.debug(tra + " " + speed + " " + bearing)

                        real_speed = float(speed)
                        real_bearing = float(bearing)

                        index_trajectory = different_tra.index(tra)

                        d = {"gen": gen, "tra": index_trajectory, "speed": real_speed, "bearing": real_bearing}
                        dfs = DataFrame(data=d, index=[gen])
                        df = df.append(dfs)

                logging.debug("Dataframe Generated")
                # small_dt = df[df.tra == 1]
                # small_dt = small_dt.drop(["tra"],1)


                sns.set(style="darkgrid")
                sns.factorplot(x="gen", y="speed", hue="tra", data=df,
                                   capsize=.2, palette="YlGnBu_d", size=6, aspect=.75)
                sns.despine()
                for el in real_points_speed:
                    plt.axhline(y=el, color='b', linestyle='--')

                sns.set(style="darkgrid")
                sns.factorplot(x="gen", y="bearing", hue="tra", data=df,
                               capsize=.2, palette="YlGnBu_d", size=6, aspect=.75)
                sns.despine()
                for el in real_points_bearing:
                    plt.axhline(y=el, color='b', linestyle='--')

                plt.show()

