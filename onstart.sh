#! /bin/bash

echo "######## TEMPERATURE MONITOR #########"
echo "Checking server time..."
sudo ntpdate-debian >> log.txt
cd /home/pi/tmonitor2
echo "Start monitoring"
echo " " >> log.txt
echo "-------------------------------------------------------" >> log.txt
echo "$(date) Start" >> log.txt
sudo python3 recordtemp.py

