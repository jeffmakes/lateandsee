#!/bin/python3
import matplotlib.pyplot as plt
import matplotlib.dates 
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
        xvalues.append(datetime.fromtimestamp(timestamp).replace(microsecond=0))
        pingtimes.append(float(d[2]))

    #dates = matplotlib.dates.date2num(xvalues)
    print(xvalues) 
    #fig, ax = plt.subplots()  # Create a figure containing a single axes.
    #ax.scatter(timestamps, pingtimes)  # Plot some data on the axes.
    plt.plot(xvalues, pingtimes)
    plt.gcf().autofmt_xdate()
    #ax.set(xlim=(1637269330, 1637275009), ylim=(8.0, 10.0))
    plt.show()
    fig.savefig("out.png", transparent=False, dpi=80)


