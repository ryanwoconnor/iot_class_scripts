#!/usr/bin/env python
from __future__ import division
from subprocess import PIPE, Popen
import psutil
import time
import requests
import socket
import configparser
import os
import sys

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def get_core_voltage():
    process = Popen(['vcgencmd', 'measure_volts', 'core'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("V")])

def main():
    cpu_temperature = get_cpu_temperature()
    cpu_usage = psutil.cpu_percent()
    core_voltage=get_core_voltage()

    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

    try:
        authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
        print(authHeader)
	url = config['DEFAULT']['url']
        print(url)
        jsonDict = {'host': str(socket.gethostname()), 'sourcetype': 'system_info', 'event': 'metric', 'fields':{'cpu_temp':cpu_temperature,'_value':cpu_temperature,'metric_name':'cpu_temperature', 'owner':config['DEFAULT']['owner']}}
        print(jsonDict)
        r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    	print(str(r))

        jsonDict = {'host': str(socket.gethostname()), 'sourcetype': 'system_info', 'event': 'metric', 'fields':{'core_voltage':core_voltage,'_value':core_voltage,'metric_name':'core_voltage', 'owner':config['DEFAULT']['owner']}}
        r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
        print(str(r))

    except:
        print("ERROR")

if __name__ == '__main__':
    main()
