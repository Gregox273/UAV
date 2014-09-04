#Photos module for using the raspberry pi camera board in a UAV
#Created 30/08/2014
#Gregory Brooks
import subprocess

class camera:
	namemodes = {'location' : 0, 'localtime' : 1, 'gpstime' : 2}
	resolution
	exif = {'on/off' : True, 'location' : True, 'time' : False, 'GPS time': True, 'satellite count' : True, 'GPS speed' : True}  
	settings = {'resolution': 'x', 'name format': "location", 'ndvi mode' : 'x', 'exif settings' : exif, 'photo directory' : '/root/photos', 'ndvi directory' : '/root/ndvi'}

	def take(self, name):
		subprocess.call(["raspistill",  "-n",  "-o", self.settings['photo directory'] + name]) 
		if self.exif['on/off'] == True:
			if self.exif['location'] == True:
				#save location to exif
			if self.exif['time'] == True:
				#save system time to exif
			if self#NOT DONE YET!!!!!!!!!!!	
	 
  

