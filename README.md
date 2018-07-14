# iot_class_scripts

This package is meant for OPIM 4895. Here we will be developing a suite of scripts for the Raspberry Pi to be used in this IoT Course. 


##Configuring Package for Splunk

This package expects you to create one file inside of the scripts directory called 'splunk_server.conf'

```
cd scripts/
touch splunk_server.conf
sudo echo "[DEFAULT]" | sudo tee -a scripts/splunk_server.conf
sudo echo "url = " | sudo tee -a scripts/splunk_server.conf
sudo echo "token = " | sudo tee -a scripts/splunk_server.conf
sudo echo "owner = " | sudo tee -a scripts/splunk_server.conf
