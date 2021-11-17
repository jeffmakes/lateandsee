#!/bin/python3

from subprocess import run
from datetime import datetime

class Pinger:

    def __init__(self, host="google.com"):
        self.host = host

    def ping(self):
        cp = run(["ping", "-c 1", "-D", self.host], capture_output=True)
        ret = cp.returncode

        if (ret == 1):
            print("Timeout")
            return PingResult(None, None, ret)
        
        if (ret == 2):
            print("Host name not known")
            return PingResult(None, None, ret)
            
        if (ret == 0):
            response = cp.stdout.splitlines()[1].decode("utf-8")
            timestamp = float(response[response.index('[')+1:response.index(']')]) #extract timestamp from between []'s
            time = response.split("time=")[1]
            return PingResult(timestamp, time, ret)

class PingResult:
     
    def __init__(self, timestamp, time, returncode):
        self.timestamp = timestamp
        self.time = time
        self.returncode = returncode
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

    def __str__(self):
        return "{} {} {} {}".format(self.timestamp, self.isotime, self.time, self.returncode)


##>>> class Complex:
#...     def __init__(self, realpart, imagpart):
#...         self.r = realpart
#...         self.i = imagpart


#cp = run(["ping", "-c 3", "google.com"], capture_output=True)
#print(cp)
p = Pinger("google.com")
#p = Pinger("sdfdsafdsafafdsasdasss.com")

print(p.ping())


