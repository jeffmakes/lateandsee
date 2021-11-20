#!/bin/python3
from measure import Measure
import threading, time
from datetime import datetime, timedelta
from plot import Plot

class LateAndSee:
    def __init__(self, interval=5, data_len=10, load_from_filename=None, write_to_filename=None, plot_filename=None):
        self.next_call = time.time()
        self.interval = interval        # interval between measurements in seconds
        self.data_len = data_len       # number of measurements to store in buffer for live plotting
        self.data = []
        self.m = Measure()
        self.outfile = None
        self.plotter = None

        if (load_from_filename):
            with open(load_from_filename, "r") as f:
                fdata = f.read().splitlines()
                self.data = fdata[(-1*self.data_len):]
                f.close()

        if (write_to_filename):
            self.outfile = open(write_to_filename, "a")

        if (plot_filename):
            self.plotter = Plot(plot_filename)

    def __exit__(self):
        if not self.outfile.closed:
            self.outfile.flush()
            self.outfile.close()

    def take_measurement(self):
        result = self.m.measure() 
        self.data.append(result)

        if len(self.data) > self.data_len:
            self.data.pop(0)

        if (self.outfile):
            self.outfile.write(result+'\n')
            self.outfile.flush()

        if (self.plotter):
            self.plotter.plot(self.data)

        self.print_data()


    def measurement_timer(self):
        print (datetime.now())
        self.take_measurement()

        self.next_call = self.next_call + self.interval
        threading.Timer(self.next_call - time.time(), self.measurement_timer).start()

    def print_data(self):
        for d in self.data:
            print(d)
        
if (__name__ == "__main__"):
    l = LateAndSee(load_from_filename="data.csv", write_to_filename="data.csv", plot_filename="out.png")
    #start = datetime.today() 
    #plot_interval = timedelta(minutes=5)
    #plot_duration = timedelta(hours=24) 
    #t = start

    l.measurement_timer()


#    with open("data.csv", "a") as f:
#        f.write(m.perform_test() + "\n")

#f.close()

