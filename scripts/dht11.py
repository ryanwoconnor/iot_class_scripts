import RPi.GPIO as GPIO
from DHT11_Python import dht11
import time
import datetime
import requests
import socket
import configparser
import os
import sys

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14

instance = dht11.DHT11(pin=4)

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))
authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
url = config['DEFAULT']['url']

result = instance.read()

jsonDict = '{"host": "'+str(socket.gethostname())+'", "sourcetype": "dht11", "event":"metric","fields":{"humidity":'+str(result.humidity)+',"_value":'+str(result.humidity)+',"metric_name":"humidity"}}{"host": "'+str(socket.gethostname())+'", "sourcetype": "dht11", "event":"metric","fields":{"temp_c":'+str(result.temperature)+',"_value":'+str(result.temperature)+',"metric_name":"temp_c"}}'
print(jsonDict)
if result.is_valid():
        try:
            r = requests.post(url,headers=authHeader,data=jsonDict,verify=False)
            print(r.text)
        except:
            print('ERROR')
