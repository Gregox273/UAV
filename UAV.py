#UAV Camera System Code
#Created 22/8/2014
#Gregory Brooks
#v0.3: Take photos every x metres
import sys, os, apm, serial, time


#Ardupilot class settings
serport = '/dev/ttyAMA0' #USB0 for USB, AMA0 for GPIO
baud = 57600
verbose = True

ap=apm.ArduPilot(serport,baud, verbose)#instance of ArduPilot class


#	loc = ap.getLocation()

