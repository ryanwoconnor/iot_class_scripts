import RPi.GPIO as GPIO
import time
import requests
import socket
import configparser
import os
import sys
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
url = config['DEFAULT']['url']

try:
    i=GPIO.input(21)
    print(str(i))	
    jsonDict = {'host': str(socket.gethostname()), 'event': 'metric', 'sourcetype':'doorsensor','fields':{'door_status':str(i),'_value':str(i),'metric_name':'door_status'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(r.text)
except:
    GPIO.cleanup()
