import datetime
import math
from typing import TextIO
import matplotlib.pyplot as plt
import numpy as np
import dateutil.parser as dp
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def main(fileName: str):
    startTime: datetime = dp.isoparse(fileName.strip(".log"))
    plt.style.use('_mpl-gallery')

    file: TextIO = open(fileName, "r")
    instructions: list = list(map(lambda line: line.strip("\n"), file.readlines()))
    create: list = list(filter(lambda line: line.split(" ")[0] == "CREATE", instructions))
    update: list = list(filter(lambda line: line.split(" ")[0] == "UPDATE", instructions))

    # Format: "variable path": [[x values], [y values]]
    plot: dict = {}

    for variables in create:
        splitList: list = variables.split(" ")
        x: float = round(dp.isoparse(splitList[5]).timestamp() - startTime.timestamp(), 3)
        y: float = float(splitList[3])
        plot[splitList[1]] = [[x], [y]]

    for variables in update:
        splitList: list = variables.split(" ")
        x: float = round(dp.isoparse(splitList[5]).timestamp() - startTime.timestamp(), 3)
        y: float = float(splitList[3])
        plot[splitList[1]][0].append(x)
        plot[splitList[1]][1].append(y)

    fig, ax = plt.subplots(); fig: Figure; ax: Axes
    plots: list = []
    for key in plot:
        plots.append(key)
        plt.plot(plot[key][0], plot[key][1], linewidth = 2.0, label = key)
    plt.legend(plots)

    ax.set(autoscale_on = True)
    xStart, xEnd = ax.get_xlim(); xStart: float; xEnd: float
    ax.xaxis.set_ticks(np.arange(math.floor(xStart), math.ceil(xEnd), 1))
    yStart, yEnd = ax.get_ylim(); yStart: float; yEnd: float
    ax.yaxis.set_ticks(np.arange(math.floor(yStart), math.ceil(yEnd), 1))
    ax.set_xlabel('time', fontsize=12)
    ax.set_ylabel('number', fontsize=12)
    fig.subplots_adjust(left = 0.05, bottom = 0.1)
    plt.show()

if __name__ == '__main__':
    main("2022-05-22T18:19:11.490949.log")