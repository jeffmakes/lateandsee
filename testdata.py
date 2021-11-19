from datetime import datetime, timedelta
from random import uniform
from time import time

host = "google.com"
target = "http://ipv4.download.thinkbroadband.com/10MB.zip"

start = datetime.today() 
delta = timedelta(minutes=5)
duration = timedelta(hours=2) 
end = start + duration
t = start

while True:
    timestamp = t.timestamp()
    isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()
    pingtime = uniform(8, 10)
    returncode = 0

    dltime = uniform(2, 5)
    speed = uniform(3, 4.5)
        
    result = "{:.3f} {} {} ms {} {} s {:.3f} Mb/s {} {} {}".format(timestamp, isotime, pingtime, returncode, dltime, speed, returncode, host, target)
    print(result)
    
    t = t + delta
    if t > end:
        break

