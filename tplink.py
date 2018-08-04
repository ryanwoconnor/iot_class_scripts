import re
import configparser
import os
import requests
import unicodedata
import socket   #for sockets
import sys  #for exit
import struct
import json
import time
import StringIO


def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)

#create an INET, STREAMing socket
try:
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    sys.stderr.write('Failed to create socket')
    sys.exit()

#sys.stderr.write("Socket Created")
#sys.stderr.write("\n")


config2 = configparser.ConfigParser()
config2.read(os.path.join(sys.path[0], 'local/tplink.conf'))
tplinks=config2['DEFAULT']

for tplink in tplinks:
    host=tplink
    #ip=tplink.split(",")[0]
    tplink_settings = config2['DEFAULT'][str(host)]
    tplink_settings = tplink_settings.split(", ")
    ip = tplink_settings[0]
    host = tplink_settings[1]


#create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.stderr.write('Failed to create socket')
        sys.exit()

    #Connect to remote server
    s.connect((ip, 9999))
 
 
    message = "AAAAJNDw0rfav8uu3P7Ev5+92r/LlOaD4o76k/6buYPtmPSYuMXlmA==".decode('base64')
 
    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        sys.stderr.write('Send to IP '+apiKeyValue+' failed')
        sys.exit()
 
 
    #get reply and print
    ciphertext = recv_timeout(s)

    #Decode Response
    key = 171
    buffer = []

    ciphertext = ciphertext.decode('latin-1')
    plaintext=''
    for char in ciphertext:
        plain = key ^ ord(char)
        key = ord(char)
        buffer.append(chr(plain))
        plaintext = ''.join(buffer)




    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))

    authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
    url = config['DEFAULT']['url']

    powerDict = plaintext[31:-3]
    powerList=powerDict.split(",")
    voltage = powerList[1].split(":")[1]
    current = powerList[0].split(":")[1]
    power = powerList[2].split(":")[1]
    total = powerList[3].split(":")[1]

    jsonDict = {'host': host, 'sourcetype': 'hs110', 'event': 'metric', 'fields':{'volts':voltage,'_value':voltage,'metric_name':'volts'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(jsonDict)
    print(r.text)

    jsonDict = {'host': host, 'sourcetype': 'hs110', 'event': 'metric', 'fields':{'amps':current,'_value':current,'metric_name':'amps'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(jsonDict)
    print(r.text)

    jsonDict = {'host': host, 'sourcetype': 'hs110', 'event': 'metric', 'fields':{'kwh':total,'_value':total,'metric_name':'kwh'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(jsonDict)
    print(r.text)

    jsonDict = {'host': host, 'sourcetype': 'hs110', 'event': 'metric', 'fields':{'watts':power,'_value':power,'metric_name':'watts'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
    print(jsonDict)
    print(r.text)

    ##Close the socket
    s.close()
