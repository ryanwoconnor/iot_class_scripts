#!/usr/bin/env python
from datetime import datetime
from time import sleep
import picamera
import os
import tinys3
import yaml
import sys
import time
import requests
import socket
import configparser


# testing
with open(os.path.join(sys.path[0])+"/"+"local/s3config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'local/splunk_server.conf'))
authHeader={'Authorization': 'Splunk '+config['DEFAULT']['logtoken']}
url = config['DEFAULT']['url']


# photo props
image_width = cfg['image_settings']['horizontal_res']
image_height = cfg['image_settings']['vertical_res']
file_extension = cfg['image_settings']['file_extension']
file_name = cfg['image_settings']['file_name']
photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
image_folder = cfg['image_settings']['folder_name']

# camera setup
camera = picamera.PiCamera()
camera.resolution = (image_width, image_height)
camera.awb_mode = cfg['image_settings']['awb_mode']

# verify image folder exists and create if it does not
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# camera warm-up time
sleep(2)

# Build filename string
filepath = image_folder + '/' + datetime.now().strftime("%Y-%m-%d-%H.%M.%S") +file_name + file_extension

if cfg['debug'] == True:
    print '[debug] Taking photo and saving to path ' + filepath
    try:
        event = str("Taking photo and saving to path " + filepath)
        jsonDict = '{"host":"'+str(socket.gethostname())+'", "sourcetype": "timelapse_s3_upload", "event": "'+str(event)+'"}'
        print(jsonDict)
        r = requests.post(url,headers=authHeader,data=jsonDict,verify=False)
        print(r.text)
    except:
        print('ERROR')

# Take Photo
camera.capture(filepath)

if cfg['debug'] == True:
    print '[debug] Uploading ' + filepath + ' to s3'
    try:
	event = str("Uploading "+filepath+" to s3")
	jsonDict = '{"host":"'+str(socket.gethostname())+'", "sourcetype": "timelapse_s3_upload", "event": "'+str(event)+'"}'
        print(jsonDict)
	r = requests.post(url,headers=authHeader,data=jsonDict,verify=False)
        print(r.text)
    except:
        print('ERROR')

# Upload to S3
conn = tinys3.Connection(cfg['s3']['access_key_id'], cfg['s3']['secret_access_key'])
f = open(filepath, 'rb')
conn.upload(filepath, f, cfg['s3']['bucket_name'],
            headers={
            'x-amz-meta-cache-control': 'max-age=60'
            })

    # Cleanup
if os.path.exists(filepath):
    os.remove(filepath)
