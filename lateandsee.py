#!/bin/python3

from subprocess import run
from datetime import datetime
from time import time
from os import path

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
            pingtime = response.split("time=")[1].split()[0]
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
        return "{} {} {} ms {} {}".format(self.timestamp, self.isotime, self.pingtime, self.returncode, self.host)

class Downloader:

    def __init__(self, target="http://ipv4.download.thinkbroadband.com/10MB.zip", timeout=30):      # https://www.thinkbroadband.com/download
        self.target = target
        self.timeout = timeout

    def download(self):
        cp = run(["curl", self.target, "--output", "/dev/null", "--max-time", str(self.timeout), "--write-out", "%{time_total} %{speed_download}"], capture_output=True)
        ret = cp.returncode
        
        if (ret == 6):
            print("Host name not known")

        elif (ret == 0):
            response = cp.stdout.splitlines()[0].decode("utf-8")
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

class Tester():

    def __init__(self):
        self.pinger = Pinger()
        self.downloader = Downloader()

    def perform_test(self):
        p = self.pinger.ping()
        d = self.downloader.download()
        timestamp = time()
        isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

        result = "{} {} {} ms {} {} s {:.3f} Mb/s {} {} {}".format(timestamp, isotime, p.pingtime, p.returncode, d.dltime, d.speed, d.returncode, p.host, d.target)
        return result 


if (__name__ == "__main__"):
    t = Tester()

    with open("data.csv", "a") as f:
        f.write(t.perform_test() + "\n")

    f.close()

