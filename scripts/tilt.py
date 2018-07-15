#!/usr/bin/env python
import RPi.GPIO as GPIO
import requests
import socket
import configparser
import os
import sys
import time

channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def alert(ev=None):
        config = configparser.ConfigParser()
        config.read(os.path.join(sys.path[0], 'splunk_server.conf'))
        authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
        url = config['DEFAULT']['url']

        jsonDict = {'host': str(socket.gethostname()), 'sourcetype': 'tilt', 'event': 'metric', 'fields':{'tilt_detected':1,'_value':1,'metric_name':'tilt_detected'}}
        r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
def loop():
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=alert, bouncetime=100)
        while True:
                pass

if __name__ == '__main__':
        try:
                loop()
        except KeyboardInterrupt:
                GPIO.cleanup()
