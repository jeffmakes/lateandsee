#!/bin/python3

from subprocess import run
from datetime import datetime
from time import time

class Pinger:

    def __init__(self, host="google.com"):
        self.host = host

    def ping(self):
        cp = run(["ping", "-c 1", "-D", self.host], capture_output=True)
        ret = cp.returncode

        if (ret == 1):
            print("Timeout")
            return PingResult(None, None, None, ret)
        
        elif (ret == 2):
            print("Host name not known")
            return PingResult(None, None, None, ret)
            
        elif (ret == 0):
            response = cp.stdout.splitlines()[1].decode("utf-8")
            timestamp = float(response[response.index('[')+1:response.index(']')]) #extract timestamp from between []'s
            pingtime = response.split("time=")[1]
            return PingResult(self.host, timestamp, pingtime, ret)
        
        else:
            print("Unknown error")

class PingResult:
     
    def __init__(self, host, timestamp, pingtime, returncode):
        self.host = host
        self.timestamp = timestamp
        self.pingtime = pingtime
        self.returncode = returncode
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

    def __str__(self):
        return "{} {} {} {} {}".format(self.timestamp, self.isotime, self.pingtime, self.returncode, self.host)

class Downloader:

    def __init__(self, target="http://ipv4.download.thinkbroadband.com/10MB.zip", timeout=30):      # https://www.thinkbroadband.com/download
        self.target = target
        self.timeout = timeout

    def download(self):
        cp = run(["curl", self.target, "--output", "/dev/null", "--max-time", str(self.timeout), "--write-out", "%{time_total} %{speed_download}"], capture_output=True)
        ret = cp.returncode
        print(ret)
        
        if (ret == 6):
            print("Host name not known")

        elif (ret == 0):
            response = cp.stdout.splitlines()[0].decode("utf-8")
            print(response)
            dltime = response.split()[0]
            speed = response.split()[1]

        else:
            print("Unknown error")

        return DownloadResult(self.target, time(), dltime, speed, ret)


class DownloadResult:
    
    def __init__(self, target, timestamp, dltime, speed, returncode):
        self.target = target
        self.timestamp = timestamp
        self.dltime = dltime
        self.speed = float(speed)/(1024*1024)
        self.returncode = returncode
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

    def __str__(self):
        return "{} {} {} s {:.3f} Mb/s {} {}".format(self.timestamp, self.isotime, self.dltime, self.speed, self.returncode, self.target)

#cp = run(["ping", "-c 3", "google.com"], capture_output=True)
#print(cp)
p = Pinger("google.com")
d = Downloader()

#p = Pinger("sdfdsafdsafafdsasdasss.com")

print(p.ping())
print(d.download())



