#!/bin/python3
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from datetime import datetime

if (__name__ == "__main__"):
    with open("data.csv", "r") as f:
        data = f.readlines()
        f.close()
    
    xvalues = []
    pingtimes = []
    for l in data:
        d = l.split()
        timestamp = float(d[0])
        xvalues.append(datetime.fromtimestamp(timestamp))
        pingtimes.append(float(d[2]))

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.scatter(xvalues, pingtimes)  # Plot some data on the axes.
    #plt.gcf().autofmt_xdate()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45)
    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
    #ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
    fig.autofmt_xdate()
    ax.set(ylim=(5, 40))
    plt.show()
    fig.savefig("out.png", transparent=False, dpi=80)


