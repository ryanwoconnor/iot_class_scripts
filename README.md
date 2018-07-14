# iot_class_scripts

This package is meant for OPIM 4895. Here we will be developing a suite of scripts for the Raspberry Pi to be used in this IoT Course. 


## Configuring Package for Splunk

This package expects you to create one file inside of the scripts directory called 'splunk_server.conf'. The following script should help you create that file. 

```
cd scripts/
touch splunk_server.conf
echo "[DEFAULT]" | tee -a splunk_server.conf
echo "url = " | tee -a splunk_server.conf
echo "token = " | tee -a splunk_server.conf
echo "owner = " | tee -a splunk_server.conf

token = Your HTTP Event Collector Token
url = The URL for the HTTP Event Collector Running in Splunk
owner = The owner for the current device. If this doesn't apply, simply leave it blank.
