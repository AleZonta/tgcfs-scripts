import logging
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    max_agent = 200
    population_size = 15
    fitness = np.arange(0, max_agent)
    fitness = fitness[::-1]
    engagement = []
    for el in fitness:
        engagement.append((float(el) - 1) / (float(population_size) - 1))

    # plt.figure(0)
    # sns.set_style("darkgrid")
    # plt.plot(fitness, engagement)
    # plt.xlabel("number of different value of fitness in the population")
    # plt.ylabel("engagement measure")
    # plt.legend()
    # plt.show()


    dinamic_step_size_old = []
    # print engagement
    for el in engagement:
        if el > 1.0:
            el = 1.0
        if el < 0.0:
            el = 0.0
        dinamic_step_size_old .append((0.001 - 0.3) * ((el - 0.0) / (1.0 - 0.0)) + 0.3)
    # print dinamic_step_size_old


    dinamic_step_size_new = []
    for el in engagement:
        dinamic_step_size_new .append((0.001 - 0.3) * ((el - 0.0) / (15.0 - 0.0)) + 0.3)
    # print dinamic_step_size_new

    # plt.figure(1)
    # sns.set_style("darkgrid")
    # plt.plot(fitness, dinamic_step_size_old, label="implement version")
    # plt.plot(fitness, dinamic_step_size_new, label="how it was supposed to be")
    # plt.xlabel("number of different value of fitness in the population")
    # plt.ylabel("step size")
    # plt.legend()


    virulence_old = []
    for el in engagement:
        if el <= 0.5:
            virulence_old.append(0.5)
        else:
            virulence_old.append(el)

    appo = []
    for el in engagement:
        appo.append((1.0 - 0.0) * ((el - 0.0) / (15.0 - 0.0)) + 0.0)

    virulence_new = []
    for el in appo:
        if el <= 0.5:
            virulence_new.append(0.5)
        else:
            virulence_new.append(el)

    # plt.figure(2)
    # sns.set_style("darkgrid")
    # plt.plot(fitness, virulence_old, label="implement version")
    # plt.plot(fitness, virulence_new, label="how it was supposed to be")
    # plt.xlabel("number of different value of fitness in the population")
    # plt.ylabel("Virulence")
    # plt.legend()

    half_max_agent = max_agent / 2
    fitness = np.arange(0, half_max_agent)

    std = []
    for el in fitness:
        std.append((1.0 - 0.0) * ((el - 0.0) / (half_max_agent - 0.0)) + 0.0)

    dinamic_step_size_old = []
    for el in std:
        if el > 1.0:
            el = 1.0
        if el < 0.0:
            el = 0.0
        dinamic_step_size_old .append((0.001 - 0.3) * ((el - 0.0) / (1.0 - 0.0)) + 0.3)

    # plt.figure(0)
    # sns.set_style("darkgrid")
    # plt.plot(fitness, dinamic_step_size_old)
    # plt.xlabel("std")
    # plt.ylabel("step size")
    # plt.legend()
    # plt.show()

    virulence_old = []
    for el in std:
        if el <= 0.5:
            virulence_old.append(0.5)
        else:
            virulence_old.append(el)

    plt.figure(2)
    sns.set_style("darkgrid")
    plt.plot(fitness, virulence_old, label="implement version")
    plt.xlabel("number of different value of fitness in the population")
    plt.ylabel("Virulence")
    plt.legend()
    plt.show()