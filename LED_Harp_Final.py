#The following program was adapted from the laser harp that we based our project on.The program still contains some of the original lines however we have made modifications to it to maximize our results
#Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
from time import sleep
from datetime import datetime
from subprocess import call
import os
import subprocess

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import numpy as np
#import python3
def callback1():
    global state
    state = 'calibrate'
string_notes = ["omxplayer -o both /home/pi/Desktop/f4.mp3","omxplayer -o both /home/pi/Desktop/g4.mp3", "omxplayer -o both /home/pi/Desktop/d4.mp3", "omxplayer -o both /home/pi/Desktop/c4.mp3", "omxplayer -o both /home/pi/Desktop/e4.mp3"]
os.system("omxplayer -o both /home/pi/Desktop/gtr-jazz.mp3")
os.system('sudo killall omxplayer.bin')
######
def signal_variance(stack): #values is 5x5 matrix corresponding to 5 samples (each row is a sample)
#function for calculating when to pluck given an alternating signal
#this function collects 5 samples, calculates their stdev
#determine pluck depending on if variance corresponds to signal being received (large variance) or not (near constant)
    means = stack.mean(axis=0) #gets average of every column
    vars = np.zeros(nstrings)
    for i in range(nstrings):
        vars[i] = np.sum((means[i]-stack[:,i])**2)/nsamples
    return np.sqrt(vars)
######

nsamples = 250 # number of samples to use for averaging signal variance
# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

nchans = 8#Numbrt of analog inputs
values= np.zeros(8)
a=np.dtype(np.int)
print('Reading MCP3008 values, press Ctrl-C to quit...')
#set up prety printer of adc values
printer = np.vectorize(lambda x: str(x).zfill(4))
for i in range(1,2):
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
nstrings = 5 #number of strings
pluckhold = .1 #number of max sec between plucks

sounds = [None]*nstrings
tpluck = [None]*nstrings
holds = [None]*nstrings
for i in range(nstrings):
    tpluck[i] = datetime.now()
    holds[i] = False

thresh_variances = np.zeros_like(values)
thresh_averages = np.zeros_like(values)

state = 'calibrate'
while True:
    if state == 'calibrate':
        print("calib...")
        LED_on = False
        while not LED_on:
            answer = raw_input('Turn on LED, type OK when done ')
            if answer == 'ok' or 'OK':
                LED_on = True
        time.sleep(1)
        os.system("omxplayer -o both /home/pi/Desktop/jingle_bells.mp3")
        os.system('sudo killall omxplayer.bin')
        stacked_values = np.zeros((nsamples,nstrings)) # will collect nsamples # of samples to calculate variance
        for i in range (len(stacked_values)):
                for j in range(nstrings):
                    # The read_adc function will get the value of the specified channel (0-7).
                    stacked_values[i,j]  = mcp.read_adc(j)
        variances_on = np.copy (signal_variance(stacked_values))
        averages_on = np.copy(np.mean(stacked_values,axis=0))

        print("variance with led on:" + str(variances_on))
        while LED_on:
            answer = raw_input('Now turn off LED, type OK when done ')
            if answer == 'ok' or 'OK':
                LED_on = False
        time.sleep (3)
        for i in range (len(stacked_values)):
            for j in range(nstrings):
                    # The read_adc function will get the value of the specified channel (0-7).
                stacked_values[i,j] = mcp.read_adc(j)
                variances_off = np.copy (signal_variance(stacked_values))
                averages_off = np.copy(np.mean(stacked_values,axis=0))

        print("variance with led off:" + str(variances_off))
        thresh_variances = variances_off + (variances_on - variances_off)*0.25
        thresh_averages = averages_off + (averages_on - averages_off)*0.90

        print("Triggering below:" + str(thresh_variances)) #this said thresh_values and gave me an error I switched to variances         
        time.sleep (3)
        print ("Calibration complete")
        #values_off = np.copy (values)
        print ("Are you ready to get funky?... Turn it on!")
        time.sleep (3)

        #thresh_values = values_off+ (values_on - raw_off)*0.5
        state = 'instrument'
    elif state == 'instrument':
        stacked_values = np.zeros((nsamples,nstrings)) # will collect 5 samples to calculate variance
        for i in range (len(stacked_values)):
                for j in range(nstrings):
                    stacked_values[i,j] = mcp.read_adc(j)
        for i in range (nstrings):
            if (datetime.now() - tpluck[i]).total_seconds()> pluckhold:
                if signal_variance(stacked_values)[i] < thresh_variances[i] and np.mean(stacked_values,axis=0)[i] < thresh_averages[i]:
                    if not holds[i]:
                        #print(stacked_values)
                        os.system(string_notes[i]) # this one is the only one that plays sound when I use it but it only works for 1 note
                        os.system('sudo killall omxplayer.bin')
                        tpluck[i] = datetime.now()
                        holds[i] = True
                else:
                    holds[i] = False
print(stacked_values)




