#!/bin/python3
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter, HourLocator
from datetime import datetime

    
class Plot:

    def __init__(self, output_filename="out.png"):
        self.output_filename = output_filename


    def plot(self, data):
        self.data = data

        xvalues = []
        pingtimes = []
        dltimes = []
        dlspeeds = []
        for l in self.data:
            d = l.split()
            timestamp = float(d[0])
            xvalues.append(datetime.fromtimestamp(timestamp))
            pingtimes.append(float(d[2]))
            dltimes.append(float(d[5]))
            dlspeeds.append(float(d[7]))

        fig, ax = plt.subplots(3, 1, sharex=True)
        
        ax[0].plot(xvalues, pingtimes, color="#57d5ff")  
        locator = HourLocator(interval=3)
        ax[0].xaxis.set_major_locator(locator)
        ax[0].xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
        locator = HourLocator(interval=1) 
        ax[0].xaxis.set_minor_locator(locator)
        
        ax[0].set_ylabel("Ping time ms")
        ax[0].set(ylim=(5, 100))
        labels = ax[2].get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        
        ax[1].plot(xvalues, dltimes, "#ffa136")  
        ax[1].set_ylabel("Download time s")
        ax[1].set(ylim=(0, 40))

        ax[2].plot(xvalues, dlspeeds, "#2affac")
        ax[2].set_ylabel("Download speed Mb/s")
        ax[2].set(ylim=(0, 5))
        
#    plt.show()
        size_px = (1600, 1000)
        dpi = 100 
        fig.set_dpi(dpi)
        fig.set_size_inches(size_px[0]/dpi, size_px[1]/dpi)
        plt.subplots_adjust(top=0.9, bottom=0.2)
        print(self.output_filename)
        fig.savefig(self.output_filename, transparent=False)


if (__name__ == "__main__"):
    with open("data.csv", "r") as f:
        data = f.readlines()
        p = Plot()
        p.plot(data)
        f.close()

