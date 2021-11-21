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
        pingtime = None

        if (ret == 1):
            print("Timeout")
        
        elif (ret == 2):
            print("Host name not known")
            
        elif (ret == 0):
            response = cp.stdout.splitlines()[1].decode("utf-8")
            #timestamp = float(response[response.index('[')+1:response.index(']')]) #extract timestamp from between []'s
            pingtime = response.split("time=")[1].split()[0]
        
        else:
            print("Unknown error")

        return PingResult(self.host, time(), pingtime, ret)

class PingResult:
     
    def __init__(self, host, timestamp, pingtime, returncode):
        self.host = host
        self.timestamp = timestamp
        self.pingtime = pingtime
        self.returncode = returncode
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

    def __str__(self):
        return "{:.3f} {} {} ms {} {}".format(self.timestamp, self.isotime, self.pingtime, self.returncode, self.host)

class Downloader:

    def __init__(self, target="http://ipv4.download.thinkbroadband.com/10MB.zip", timeout=30):      # https://www.thinkbroadband.com/download
        self.target = target
        self.timeout = timeout

    def download(self):
        cp = run(["curl", self.target, "--output", "/dev/null", "--max-time", str(self.timeout), "--write-out", "%{time_total} %{speed_download}"], capture_output=True)
        ret = cp.returncode
        dltime = None
        speed = None
        
        if (ret == 6):
            print("Host name not known")

        elif (ret == 0):
            response = cp.stdout.splitlines()[0].decode("utf-8")
            dltime = response.split()[0]
            speed = float(response.split()[1])/(1024*1024)

        else:
            print("Unknown error")

        return DownloadResult(self.target, time(), dltime, speed, ret)


class DownloadResult:
    
    def __init__(self, target, timestamp, dltime, speed, returncode):
        self.target = target
        self.timestamp = timestamp
        self.dltime = dltime
        self.speed = speed
        self.returncode = returncode
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()

    def __str__(self):
        return "{} {} {} s {:.3f} Mb/s {} {}".format(self.timestamp, self.isotime, self.dltime, self.speed, self.returncode, self.target)

class MeasureResult:
    def __init__(self, timestamp, ping_returncode, ping_time, dl_returncode, dl_time, dl_speed, ping_host, dl_target):
        self.timestamp = timestamp
        self.isotime = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()
        self.ping_returncode = ping_returncode
        self.ping_time = ping_time
        self.dl_returncode = dl_returncode
        self.dl_time = dl_time
        self.dl_speed = dl_speed
        self.ping_host = ping_host
        self.dl_target = dl_target

    def __str__(self):
        try:
            s = "{:.3f} {} {} ms {} {} s {:.3f} Mb/s {} {} {}".format(self.timestamp, self.isotime, self.ping_time, self.ping_returncode, self.dl_time, self.dl_speed, self.dl_returncode, self.ping_host, self.dl_target)
        except:
            s = "" 
        return s

class Measure():

    def __init__(self):
        self.pinger = Pinger()
        self.downloader = Downloader()

    def measure(self):
        p = self.pinger.ping()
        d = self.downloader.download()
        timestamp = time()

        result = MeasureResult(timestamp, p.returncode, p.pingtime, d.returncode, d.dltime, d.speed, p.host, d.target)
        return result 



