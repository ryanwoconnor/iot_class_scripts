import RPi.GPIO as GPIO
import time
import requests
import socket
import configparser
import os
import sys
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
url = config['DEFAULT']['url']

try:
    i=GPIO.input(16)
    jsonDict = '{"host": "'+str(socket.gethostname())+'", "event": "metric", "fields":{"water_motion":'+str(i)+',"_value":'+str(i)+',"metric_name":"water_motion"}}'
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(jsonDict)
    print(r.text)
except:
    GPIO.cleanup()


