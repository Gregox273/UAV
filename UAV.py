#UAV Camera System Code
#Created 22/8/2014
#Gregory Brooks
import apm, serial, time, photos
#import sys, os?


#Ardupilot class settings
serport = '/dev/ttyAMA0' #USB0 for USB, AMA0 for GPIO
baud = 57600
verbose = True

ap=apm.ArduPilot(serport,baud, verbose)#instance of ArduPilot class

#while 1:
#	loc = ap.getLocation()
#	print loc
#	time.sleep(1)
cam = photos.camera(ap)
for x in range (0,10):
	time.sleep(1)
	loc, att, bear = cam.take()
	print loc
	print att
	print bear
	print ""
	print"-----------------"
	print ""
