#!/bin/python3
from measure import Measure
from serve import Serve
import threading, time
from datetime import datetime, timedelta
from time import sleep
from plot import Plot
import sys, os


class LateAndSee:
    def __init__(self, interval=5, plot_duration=24*60*60, load_from_filename=None, write_to_filename=None, plot_filename=None):
        self.next_call = time.time()
        self.interval = interval        # interval between measurements in seconds
        self.data_len = int(24 * 60 * (60/interval))   # number of measurements to store in buffer for live plotting
        self.data = []
        self.m = Measure()
        self.outfile = None
        self.plotter = None

        if (load_from_filename):
            with open(load_from_filename, "r") as f:
                timestamps = []
                fdata = f.read().splitlines()
                
                for l in fdata:
                    timestamps.append(float(l.split()[0]))
                begin_idx = next(i for i,v in enumerate(timestamps) if v > (time.time()-plot_duration) )    #find index of first timestamp after plot_duration seconds ago
                print("Plotting from timestamp {}".format(timestamps[begin_idx]))
                self.data = fdata[begin_idx:]
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
        result = str(self.m.measure())

        if (result):        # if there is an error, eg. no network, result will be zero-length
            self.data.append(result)

            if len(self.data) > self.data_len:
                self.data.pop(0)

            if (self.outfile):
                self.outfile.write(result+'\n')
                self.outfile.flush()

    def measurement_timer(self):
        print (datetime.now())
        self.take_measurement()

        self.next_call = self.next_call + self.interval
        self.timer = threading.Timer(self.next_call - time.time(), self.measurement_timer).start()

    def print_data(self):
        for d in self.data:
            print(d)

    def get_data(self):
        return self.data

    def plot_data(self):
        if (self.plotter):
            self.plotter.plot(self.data)

    def get_interval(self):
        return self.interval
    

if (__name__ == "__main__"):
    try:
        l = LateAndSee(interval = 60, load_from_filename="data.csv", write_to_filename="data.csv", plot_filename="out.png")
        s =  Serve()
        print("Beginning measurement")

        l.measurement_timer()
        while True:
            sleep(l.get_interval())
            l.plot_data()

    except KeyboardInterrupt:
        l.__exit__()
        s.stop()
        print("Bye")

        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

