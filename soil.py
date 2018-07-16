# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#print("soil_moisture_level="+str(mcp.read_adc(3)))


authHeader={'Authorization': 'Splunk E4D0E545-6D3B-4411-9495-0D2E78DF5AE8'}
url='http://l1barcv-rwo0601.business.uconn.edu:8090/services/collector/event'

jsonDict = {'host': 'pi_aquaponics1', 'sourcetype':'etoput:soilmoisture', 'event': 'metric', 'fields':{'moisture_level':str(mcp.read_adc(3)), '_value':str(mcp.read_adc(3)), "metric_name":'moisture_level'}}
print(str(jsonDict))
r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
print r.text
