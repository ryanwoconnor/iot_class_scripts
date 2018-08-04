import os
import glob
import time
import socket
import configparser
import requests
import sys

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
url = config['DEFAULT']['url']

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(url, authHeader):
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        jsonDict = {'host': str(socket.gethostname()), 'event': 'metric', 'fields':{'water_temp':str(temp_f),'_value':str(temp_f),'metric_name':'water_temp'}}
        r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
        print(r.text)
        return "temp_c="+str(temp_c)+" "+"temp_f="+str(temp_f)

print(read_temp(url, authHeader))
