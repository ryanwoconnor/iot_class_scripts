#!/usr/bin/python
from sense_hat import SenseHat
import time
import socket
import sys
import requests
import json
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

authHeader={'Authorization': 'Splunk '+config['DEFAULT']['logtoken']}
url = config['DEFAULT']['url'] 

sense = SenseHat()
sense.clear()

p = (227, 2, 128)
o = (240, 96, 65)
b = (0, 0, 0)
w = (255,255,255)


arrow_splunk = [
p,w,w,p,p,p,p,p,
p,p,w,w,p,p,p,p,
p,p,p,w,w,p,p,p,
p,p,p,p,p,w,w,p,
p,p,p,p,p,w,w,o,
p,p,p,w,w,o,o,o,
p,p,w,w,o,o,o,o,
p,w,w,o,o,o,o,o
]

sense.set_pixels(arrow_splunk)

def get_Host_name_IP():
    try:
        host_name = socket.gethostname()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        
        #host_ip = socket.gethostbyname(socket.getfqdn())
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
        return("Hostname: " + host_name + " IP Address: " + host_ip)
    except:
        print("Unable to get Hostname and IP")

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
    
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)


    o = sense.get_orientation()
    gyro_y = round(o["pitch"], 0)
    gyro_x = round(o["roll"], 0)
    gyro_z = round(o["yaw"], 0)

    jsonDict = {"host":"weatherstation01","sourcetype":"weather_data","event": {"temp":temp,"humidity":humidity,"pressure":pressure,"acc_x":x, "acc_y":y,"acc_z":z, "gyro_z":gyro_z,"gyro_y":gyro_y,"gyro_x":gyro_x}}
    #print(jsonDict) 
    for event in sense.stick.get_events():
        if event.action == 'pressed' and event.direction == 'up':
            sense.show_message(get_Host_name_IP(), scroll_speed=(0.08), back_colour= [227,2,128])
            sense.set_pixels(arrow_splunk)
        if event.action == 'pressed' and event.direction == 'down':
            pass
        if event.action == 'pressed' and event.direction == 'right':
            pass
        if event.action == 'pressed' and event.direction == 'middle':
            r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
            print(r.status_code)
            sense.show_message("Temperature: " + str(temp) + " Humidity:" + str(humidity) + " Pressure:" + str(pressure), scroll_speed=(0.08), back_colour= [227,2,128])
            sense.set_pixels(arrow_splunk)
    time.sleep(1)

sense.clear()
