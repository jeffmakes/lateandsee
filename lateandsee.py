#!/bin/python3
from measure import Measure
import threading, time
from datetime import datetime, timedelta


class LateAndSee:
    def __init__(self, interval=5, data_len=10):
        self.next_call = time.time()
        self.interval = interval        # interval between measurements in seconds
        self.data_len = data_len       # number of measurements to store in buffer for live plotting
        self.data = []
        self.m = Measure()

    def take_measurement(self):
        result = self.m.measure() 
        #print(result)
        self.data.append(result)
        for d in self.data:
            print(d)

        if len(self.data) > self.data_len:
            self.data.pop(0)

    def measurement_timer(self):
        #global next_call
        #global interval
        print (datetime.now())
        self.take_measurement()

        self.next_call = self.next_call + self.interval
        threading.Timer(self.next_call - time.time(), self.measurement_timer).start()
        
if (__name__ == "__main__"):
    l = LateAndSee()
    #start = datetime.today() 
    #plot_interval = timedelta(minutes=5)
    #plot_duration = timedelta(hours=24) 
    #t = start

    l.measurement_timer()


#    with open("data.csv", "a") as f:
#        f.write(m.perform_test() + "\n")

#f.close()

