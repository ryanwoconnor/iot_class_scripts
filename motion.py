import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

try:
    i=GPIO.input(16)
    authHeader={'Authorization': 'Splunk 8ce81b64-f5d8-4753-9d6e-f9bfc58ba420'}
    url='http://l1barcv-rwo0601.business.uconn.edu:8090/services/collector/event'
    jsonDict = {'host': 'pi_aquaponics1', 'event': 'metric', 'fields':{'water_motion':str(i),'_value':str(i),'metric_name':'water_motion'}}
    r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
except:
    GPIO.cleanup()


