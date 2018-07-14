#!/usr/bin/env python
from __future__ import division
from subprocess import PIPE, Popen
import psutil
import time
import requests
import socket
import configparser

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def main():
    cpu_temperature = get_cpu_temperature()
    cpu_usage = psutil.cpu_percent()
#    disk = psutil.disk_usage('/')
#    disk_total = disk.total / 2**30     # GiB.
#    disk_used = disk.used / 2**30
#    disk_free = disk.free / 2**30
#    disk_percent_used = disk.percent

    config = configparser.ConfigParser()
    config.read('splunk_server.conf')

    try:
        authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
        url = config['DEFAULT']['url']
        jsonDict = {'host': str(socket.gethostname()), 'sourcetype': 'system_info', 'event': 'metric', 'fields':{'cpu_temp':str(cpu_temperature),'_value':str(cpu_temperature),'metric_name':'cpu_temperature', 'owner':config['DEFAULT']['owner']}}
        r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    except:
        print("ERROR")

if __name__ == '__main__':
    main()
