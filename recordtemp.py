# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
# Modified for thermistor readings by J. Katz 2018-01-12

import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import datetime
import math
import os
# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# The resistor value
R = 10000
# Beta coefficient
B = 3950
# Number of samples to average
N = 20
os.setuid(1000)
# The data file name is the system date
#path = datetime.datetime.today().strftime("%Y-%m-%d") + ".csv"

path = "temperatures.csv"
try:
    # Test for a data file
    f = open(path, "r")
    f.close()
    with open("log.txt", "a") as log:
        log.write("Writing to existing file: " + path + "\n")
    print("Existing data file: " + path)
except:
    # If data file doesn't exist, create it and add column headings
    with open(path, "a+") as f:
        f.write("s1, s2, s3, s4, s5, s6, s7, s8, Time\n")
    with open("log.txt", "a+") as log:
        log.write("Creating new file: " + path + "\n")
    print("New data file: " + path)
# Main program loop
while True:
    # Store groups of samples for later averaging
    samples = [0]*N*8
    avgvalues = [0]*8
    for j in range(N):
        # Read all the ADC channel values in a list.
        # Expecting output on all 8 channels.
        values = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
        # Store the set of 8 values in a longer list
        samples[j*8:j*8+8] = values
        #time.sleep(30)
        time.sleep(1)
    for k in range(8):
        tot = sum(samples[k::8])
        n = len(samples[k::8])
        resist = R / ( 1023 / ( tot / n ) - 1 )
        st = math.log( resist / 10000 ) / B
        st += 1 / ( 25 + 273.15 )
        st = 1 / st
        st -= 273.15
        st = 9 * st/5 + 32   
        avgvalues[k] = round(st,1)        
    # Log the ADC values.
    logtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a") as f:
        f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, '.format(*avgvalues) + logtime + "\n")
    print(logtime, ": true")
    minute = int(datetime.datetime.now().strftime("%M"))
    with open("log.txt", "r") as log:
        for line in log:
            pass
        last = line
    
    if (!minute % 10) :
	os.sytem("R CMD BATCH --no-save --no-restore upload.R")
    if (minute >= 50) and (last != "git: true\n")  :
        #print('make plot')
        #with open("log.txt", "a") as log:
            #log.write("make plot\n")
        #os.system("R CMD BATCH --no-save --no-restore makeplot.R")
        try:
            print('push to git...')
            with open("log.txt", "a") as log:
                log.write("git push:" + logtime + "\n")
            os.system("git config user.email = 'jonkatz2@gmail.com'")
            os.system("git config user.name = 'jon'")
            os.system("git add --all >> log.txt")
            os.system("git commit -m 'autocommit " + logtime +"' >> log.txt")
            os.system("git push origin master >> log.txt")
            with open("log.txt", "a") as log:
                log.write("git: true\n")
        except:
            print('push to git failed')
	    with open("log.txt", "a") as log:
		log.write("push to git failed\n")    
    else: 
        with open("log.txt", "a") as log:
            log.write("git: false\n")
#    nowint = int(datetime.datetime.now().strftime("%H%M%S"))
    #with open("log.txt", "r") as log:
    #    for line in log:
    #        pass
    #    last = line
#    if (nowint < 1001):
        #with open("log.txt", "a") as log:
        #    log.write("reboot: true\n")
#        os.system("sudo reboot")
    
