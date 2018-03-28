import logging
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/O1.txt"
    with open(path, 'rb') as f:
        content = f.readlines()

        x = np.arange(0, len(content))


        plt.plot(x, content)
        plt.xlim(0, 1000)

        plt.show()