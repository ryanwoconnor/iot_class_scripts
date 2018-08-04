# iot_class_scripts

This package is meant for OPIM 4895. Here we will be developing a suite of scripts for the Raspberry Pi to be used in this IoT Course. 


## Configuring Package for Splunk

This package expects you to create one file inside of the scripts directory called 'splunk_server.conf'. The following script should help you create that file. 

```
cd iot_class_scripts/
mkdir local/
cp splunk_server.conf local/
```

Once you've created the file, fill in the approprate sections. Below are definitions for each key. 

token = Your HTTP Event Collector Token

url = The URL for the HTTP Event Collector Running in Splunk

owner = The owner for the current device. If this doesn't apply, simply leave it blank.


## Configuring TP-Link Script

This package allows you to query multiple TP-Link HS110 Devices. You can screate a tplink.conf file inside of the local directory as well. There is a sample file called tplink.conf that will show you how to configure this. 

```
cd iot_class_scripts/
mkdir local/
cp tplink.conf local/
```

Once you have the file in place, created a comma separated entry on each line for IP Address and hostname as shown in the file. 
