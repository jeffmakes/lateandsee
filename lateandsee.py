#!/bin/python3
from measure import Measure
import threading, time
from datetime import datetime, timedelta

next_call = time.time()
interval = 5        # interval between measurements in seconds
m = Measure()

def take_measurement():
    print(m.measure())


def measurement_timer():
    global next_call
    global interval
    print (datetime.now())
    take_measurement()

    next_call = next_call + interval
    threading.Timer(next_call - time.time(), measurement_timer).start()
    
if (__name__ == "__main__"):

    start = datetime.today() 
    plot_interval = timedelta(minutes=5)
    plot_duration = timedelta(hours=24) 
    t = start

    measurement_timer()


#    with open("data.csv", "a") as f:
#        f.write(m.perform_test() + "\n")

#f.close()

