import logging
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def printGraphStepSize(path, n):
    lines_interesting_agent = []
    lines_interesting_classifier = []
    with open(path) as f:
        lines = f.readlines()

        for el in lines:
            if "NFO: AGENT new step size ->" in el:
                lines_interesting_agent.append(float(el.replace("INFO: AGENT new step size -> ", "").replace("\n", "")))
            if "NFO: CLASSIFIER new step size ->" in el:
                lines_interesting_classifier.append(
                    float(el.replace("INFO: CLASSIFIER new step size -> ", "").replace("\n", "")))

    x = np.arange(0, len(lines_interesting_agent))
    x1 = np.arange(0, len(lines_interesting_classifier))

    plt.figure(n)
    sns.set_style("darkgrid")
    plt.plot(x, lines_interesting_agent, label='agent step size')
    plt.plot(x1, lines_interesting_classifier, label='classifier step size')
    plt.legend()


def printGraphVirulence(path, n):
    lines_interesting_agent = []
    lines_interesting_classifier = []
    with open(path) as f:
        lines = f.readlines()

        for el in lines:
            if "NFO: AGENT new virulence ->" in el:
                lines_interesting_agent.append(float(el.replace("INFO: AGENT new virulence -> ", "").replace("\n", "")))
            if "NFO: CLASSIFIER new virulence ->" in el:
                lines_interesting_classifier.append(
                    float(el.replace("INFO: CLASSIFIER new virulence -> ", "").replace("\n", "")))

    x = np.arange(0, len(lines_interesting_agent))
    x1 = np.arange(0, len(lines_interesting_classifier))

    plt.figure(n)
    sns.set_style("darkgrid")
    plt.plot(x, lines_interesting_agent, label='agent virulence')
    plt.plot(x1, lines_interesting_classifier, label='classifier virulence')
    plt.legend()


def printGraphTogether(path, n):
    lines_interesting_agent = []
    lines_interesting_classifier = []
    lines_interesting_agent_virulence = []
    lines_interesting_classifier_virulence = []
    with open(path) as f:
        lines = f.readlines()

        for el in lines:
            if "NFO: AGENT new step size ->" in el:
                lines_interesting_agent.append(float(el.replace("INFO: AGENT new step size -> ", "").replace("\n", "")))
            if "NFO: CLASSIFIER new step size ->" in el:
                lines_interesting_classifier.append(
                    float(el.replace("INFO: CLASSIFIER new step size -> ", "").replace("\n", "")))
            if "NFO: AGENT new virulence ->" in el:
                lines_interesting_agent_virulence.append(float(el.replace("INFO: AGENT new virulence -> ", "").replace("\n", "")))
            if "NFO: CLASSIFIER new virulence ->" in el:
                lines_interesting_classifier_virulence.append(
                    float(el.replace("INFO: CLASSIFIER new virulence -> ", "").replace("\n", "")))


    x = np.arange(0, len(lines_interesting_agent))
    x1 = np.arange(0, len(lines_interesting_classifier))
    x2 = np.arange(0, len(lines_interesting_agent_virulence))
    x3 = np.arange(0, len(lines_interesting_classifier_virulence))

    plt.figure(n)
    sns.set_style("darkgrid")
    plt.plot(x, lines_interesting_agent, label='agent step size')
    plt.plot(x1, lines_interesting_classifier, label='classifier step size')
    plt.plot(x2, lines_interesting_agent_virulence, label='classifier virulence')
    plt.plot(x3, lines_interesting_classifier_virulence, label='classifier virulence')
    plt.legend()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/2/classifier.log"
    printGraphStepSize(path, 1)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/3/classifier.log"
    printGraphStepSize(path, 2)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/4/classifier.log"
    printGraphVirulence(path, 3)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/5/classifier.log"
    printGraphVirulence(path, 4)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/6/classifier.log"
    printGraphTogether(path, 5)

    path = "/Users/alessandrozonta/Desktop/Experiment-TestOne/7/classifier.log"
    printGraphTogether(path, 6)

    plt.show()