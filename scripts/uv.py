# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests
import socket
import configparser
import os
import sys
import time

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


config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'splunk_server.conf'))
authHeader={'Authorization': 'Splunk '+config['DEFAULT']['token']}
url = config['DEFAULT']['url']

jsonDict = {'host': str(socket.gethostname()), 'sourcetype': 'guva-s12sd', 'event': 'metric', 'fields':{'uv_index':str(mcp.read_adc(2)),'_value':str(mcp.read_adc(2)),'metric_name':'uv_index'}}

r = requests.post(url,headers=authHeader,json=jsonDict,verify=False)
print r.text
