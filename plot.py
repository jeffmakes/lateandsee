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
    dlspeeds = []
    for l in data:
        d = l.split()
        timestamp = float(d[0])
        xvalues.append(datetime.fromtimestamp(timestamp))
        pingtimes.append(float(d[2]))
        dltimes.append(float(d[5]))
        dlspeeds.append(float(d[7]))

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    #locator = AutoDateLocator()
    locator = HourLocator(interval=3)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
    locator = HourLocator(interval=1) 
    ax.xaxis.set_minor_locator(locator)
    
    ax.set_ylabel("Ping time ms")
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')

    twin1 = ax.twinx()
    twin2 = ax.twinx()
    ping_plot = ax.plot(xvalues, pingtimes, label="Ping time")  # Plot some data on the axes.
    dltime_plot = twin1.plot(xvalues, dltimes, label="Download time", color="#0f0f0f")  # Plot some data on the axes.
    dlspeed_plot = twin2.plot(xvalues, dlspeeds, label="Download speed")  # Plot some data on the axes.
    ax.set_ylim(5, 40)
    twin1.set_ylim(1, 20)
    twin2.set_ylim(0, 10)
    
#   ax[1].plot(xvalues, dltimes)  # Plot some data on the axes.
#    ax[1].set_ylabel("Download time s")
    #plt.gcf().autofmt_xdate()
    #ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
    #fig.autofmt_xdate()
#    ax[1].set(ylim=(5, 40))
    plt.show()
    fig.savefig("out.png", transparent=False, dpi=80)


