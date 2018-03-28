import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    df = pd.read_csv("/Users/alessandrozonta/Documents/trajectoryTesting/matrix.csv", header=None)
    df = df[df.columns].astype(float)

    sns.heatmap(df, cmap="YlGnBu")
    plt.show()
