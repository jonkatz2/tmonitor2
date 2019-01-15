#! /bin/bash

cd /home/pi/tmonitor2
echo ""
echo "######## TEMPERATURE MONITOR #########"
echo "Checking server time..."
sudo ntpdate-debian >> log.txt
sudo chown pi:pi log.txt
echo "Start monitoring"
echo " " >> log.txt
echo "-------------------------------------------------------" >> log.txt
echo "$(date) Start" >> log.txt
sudo python3 recordtemp.py

