#!/bin/python3
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter, HourLocator
from datetime import datetime

if (__name__ == "__main__"):
    with open("data.csv", "r") as f:
        data = f.readlines()
        f.close()
    
    xvalues = []
    pingtimes = []
    dltimes = []
    speeds = []
    for l in data:
        d = l.split()
        timestamp = float(d[0])
        xvalues.append(datetime.fromtimestamp(timestamp))
        pingtimes.append(float(d[2]))
        dltimes.append(float(d[5]))
        speeds.append(float(d[7]))

    fig, ax = plt.subplots(2, 1, sharex=False)  # Create a figure containing a single axes.
    ax[0].plot(xvalues, pingtimes)  # Plot some data on the axes.
    #locator = AutoDateLocator()
    locator = HourLocator(interval=3)
    ax[0].xaxis.set_major_locator(locator)
    ax[0].xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
    locator = HourLocator(interval=1) 
    ax[0].xaxis.set_minor_locator(locator)
    
    ax[0].set_ylabel("Ping time ms")
    ax[0].set(ylim=(5, 40))
    labels = ax[0].get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    
    ax[1].plot(xvalues, dltimes)  # Plot some data on the axes.
    ax[1].set_ylabel("Download time s")
    #plt.gcf().autofmt_xdate()
    #ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
    #fig.autofmt_xdate()
    ax[1].set(ylim=(5, 40))
    plt.show()
    fig.savefig("out.png", transparent=False, dpi=80)


