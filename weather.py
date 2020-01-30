#!/usr/bin/python
from sense_hat import SenseHat
import time
import os
import sys
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

authHeader={'Authorization': 'Splunk '+config['DEFAULT']['logtoken']}
url = config['DEFAULT']['url'] 

sense = SenseHat()
sense.clear()

try:
      while True:
           temp = sense.get_temperature()
           temp = round(temp, 1)
           print("Temperature C",temp) 

           humidity = sense.get_humidity()  
           humidity = round(humidity, 1)  
           print("Humidity :",humidity)  
           
           pressure = sense.get_pressure()
           pressure = round(pressure, 1)
           print("Pressure:",pressure)
           
           jsonDict = {"host":"weatherstation01","sourcetype":"weather","event": {"Temperature":temp,"Humidity":humidity,"Pressure":pressure}}
           
           r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
           
           sense.show_message("Temperature C" + str(temp) + "Humidity:" + str(humidity) + "Pressure:" + str(pressure), scroll_speed=(0.08), back_colour= [0,0,200])
           
           time.sleep(1)
except KeyboardInterrupt:
      pass

sense.clear()
