#! /bin/bash

sudo ntpdate-debian
cd /home/pi/tmonitor2
sudo echo "$(date) Start" >> log.txt
sudo python3 recordtemp.py

