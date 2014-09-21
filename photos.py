#Photos module for using the raspberry pi camera board in a UAV
#Created 30/08/2014
#Gregory Brooks
import subprocess, apm

class camera:
        quality  = "50"                 #0 to 100, not linear!
	namemodes = {'location' : 0, 'localtime' : 1, 'gpstime' : 2}
	ndvi = {'overwrite' : 0, 'copy' : 1, 'off' : 2}
	exif = {'on/off' : True, 'location' : True, 'time' : False, 'GPS time': True, 'satellite count' : True, 'GPS speed' : True}  
	settings = {'resolution': quality, 'name format': namemodes['location'], 'ndvi mode' : ndvi['copy'], 'photo directory' : '/root/photos', 'ndvi directory' : '/root/ndvi'}

	def take(self):
		command =  "raspistill " + "-n " + "-o " + self.settings['photo directory'] + name]
		if self.exif['on/off'] == True:
			if self.exif['location'] == True:
				#save location to exif
			if self.exif['time'] == True:
				#save system time to exif
                        else if self.exif['GPS time'] == True:
                                #save GPS time to exif
                        if self.exif['satellite count'] == True:
				#save satellite count to exif
                        if self.exif['GPS speed'] == True:
				#save GPS speed to exif

                                
                subprocess.call(command)
			
	 
  

