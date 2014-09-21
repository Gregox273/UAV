#Photos module for using the raspberry pi camera board in a UAV
#Created 30/08/2014
#Gregory Brooks
import subprocess, apm, thread, math





#FIX GPS COORDS FUNCTION THEN ADD NDVI FUNCTIONALITY (THREADS)




class camera:
	def __init__(self,ap):
		self.ap = ap
		print "ap imported"
	quality = "50 " #0 to 100, not linear!      
	namemodes = {'location' : 0, 'localtime' : 1, 'gpstime' : 2}
	ndvi = {'overwrite' : 0, 'copy' : 1, 'off' : 2}
	exif = {'on/off' : True, 'location' : True, 'time' : False, 'GPS time': False, 'satellite count' : False, 'GPS speed' : False}  
	settings = {'resolution': quality, 'name format': namemodes['location'], 'ndvi mode' : ndvi['copy'], 'photo directory' : '/root/photos/', 'ndvi directory' : '/root/ndvi'}

	def take(self):
		print "taking photo"
		command =  "raspistill " + "-n " + "-q " + self.quality + "-t " + "50 "
		if self.exif['on/off'] == True:
			if self.exif['location'] == True:
				loc = self.ap.getLocation()
				print loc
				lat = self.ddtodms(loc['lat'])
				lon = self.ddtodms(loc['lon'])
				command = command + "-x GPS.GPSLatitude=" + str(lat['deg']) + "/1," + str(lat['min']) + "/1," + str(lat['sec']) + "/100 "
				command = command + "-x GPS.GPSLongitude=" + str(lon['deg']) + "/1," + str(lon['min']) + "/1," + str(lon['sec']) + "/100 "
#Do these later------------------------------------------------------
			#if self.exif['time'] == True:
				#save system time to exif
                        #else if self.exif['GPS time'] == True:
                                #save GPS time to exif
                        #if self.exif['satellite count'] == True:
				#save satellite count to exif
                        #if self.exif['GPS speed'] == True:
				#save GPS speed to exif
#--------------------------------------------------------------------
		name = "x"
		if self.settings['name format'] == 0:
			name = str(loc['lat']) + "_" + str(loc['lon'])
   		command = command + "-o " + self.settings['photo directory'] + name + ".jpg"                             
                print "calling:" +  command
		subprocess.call(command,shell=True)
			
	 
  	def ddtodms(self, dd):
		coords = {'deg': 0, 'min' : 0, 'sec' : 0}
		coords['deg'] = math.trunc(dd)
		coords['min'] = math.trunc(60*(dd - coords['deg']))
		coords['sec'] = math.trunc(3600*(dd - coords['deg'] - coords['min']/60))
		return coords

#use threads for ndvi conversion (so the program doesn't slow down)
#anything else to thread?
