#Photos module for using the raspberry pi camera board in a UAV
#Created 30/08/2014
#Gregory Brooks
import subprocess, apm, thread, math
from decimal import *






class camera:
        def __init__(self,ap):
                self.ap = ap
                print "ap imported"
                quality = "50 " #0 to 100, not linear!      
                namemodes = {'location' : 0, 'localtime' : 1, 'gpstime' : 2}
                ndvi = {'overwrite' : 0, 'copy' : 1, 'off' : 2}
                exif = {'on/off' : True, 'location' : True, 'time' : False, 'GPS time': False, 'satellite count' : False, 'GPS speed' : False}  
                settings = {'resolution': quality, 'name format': namemodes['location'], 'ndvi mode' : ndvi['copy'], 'photo directory' : '/root/photos/', 'ndvi directory' : '/root/ndvi'}
                R = 6371000 #radius of earth/m
                hAngle = 54#angle of view/degrees
                vAngle = 41

        def take(self):
                print "taking photo"
                command =  "raspistill " + "-n " + "-q " + self.quality + "-t " + "50 "
                loc = self.ap.getLocation()
                att = self.ap.getAttitude()
                alt = self.ap.getAltitude()
                bear = self.ap.getHeading()
                if self.exif['on/off'] == True:
                        if self.exif['location'] == True:
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
                return (loc, att, bear) 
                        
         
        def ddtodms(self, dd):
                dd = Decimal(str(dd))
                coords = {'deg': 0, 'min' : 0, 'sec' : 0}
                coords['deg'] = int(dd)
                coords['min'] = int(60*(dd - coords['deg']))
                dp = Decimal('0.0001') #3dp
                coords['sec'] = Decimal(3600*(dd - coords['deg'] - Decimal(coords['min'])/60)).quantize(dp)
                coords['deg'] = str(coords['deg'])#standard string output
                coords['min'] = str(coords['min'])
                if coords['sec'] < 0:
                    coords['sec'] = str(0 - coords['sec'])
                    coords['deg'] = '-' + coords['deg']
                else:
                    coords['sec'] = str(coords['sec'])

                return coords

        def getcorners(loc, bear, att, alt, hAngle, vAngle):
                lat = degtorad(loc['lat'])
                lon = degtorad(loc['lon'])
                hdg = degtorad(bear)
                hAngle = degtorad(hAngle)
                vAngle = degtorad(vAngle)
            
                #distances from vertically under camera to each edge of the photo
                tr = {'lat': 0, 'lon': 0, 'dist': 0, 'theta':0}
                br = {'lat': 0, 'lon': 0, 'dist': 0, 'theta': 0}
                bl = {'lat': 0, 'lon': 0, 'dist': 0, 'theta': 0}
                tl = {'lat': 0, 'lon': 0, 'dist': 0, 'theta': 0}
                corners = [tr,br,bl,tl]
                corners = vector(att['pitch'], att['roll'], hAngle, vAngle, alt, hdg, corners)
                    
                for x in range (0,3):
                        dest = corners(loc['lat'], loc['lon'], corners[x]['theta'],Decimal(corners[x]['distance'])/R)
                        corners[x]['lat'] = dest['lat']
                        corners[x]['lon'] = dest['lon']
    
    
    
        def degtorad(angle):
                return (Decimal(angle*math.pi)/180)

        def vector(pitch,roll,hAngle,vAngle,alt,hdg, corners):
                #returns each corner of the photo as a vector (magnitude and direction) in the ground plane
                #(from the 2D coordinates of the aircraft
                hAngle = Decimal(hAngle)/2
                vAngle = Decimal(vAngle)/2
                disp = {'tr' : 0, 'br' : 0, 'bl': 0, 'tl': 0}
                
                fwd = alt * Decimal(math.tan(vAngle + pitch))
                bwd = alt * Decimal(math.tan(vAngle - pitch))
                left= alt * Decimal(math.tan(hAngle + roll))
                right=alt * Decimal(math.tan(hAngle - roll))

                corners[0]['dist'] = Decimal(fwd^2+right^2).sqrt()
                corners[1]['dist'] = Decimal(bwd^2+right^2).sqrt()
                corners[2]['dist'] = Decimal(bwd^2+left^2).sqrt()
                corners[3]['dist'] = Decimal(fwd^2+left^2).sqrt()

                corners[0]['theta'] = Decimal(hdg+math.atan(Decimal(right)/fwd))
                corners[1]['theta'] = Decimal(hdg+math.pi-math.atan(Decimal(right)/bwd))
                corners[2]['theta'] = Decimal(hdg+math.pi+math.atan(Decimal(left)/bwd))
                corners[4]['theta'] = Decimal(hdg-math.atan(Decimal(left)/fwd))
                return corners
    
        def corners(p,l,t,d):
                #based on formula from http://www.movable-type.co.uk/scripts/latlong.html
                dest = {'lat': 0, 'lon': 0}
                dest['lat'] = Decimal(math.asin(math.sin(p)*math.cos(d)+math.cos(p)*math.sin(d)*math.cos(t)))
                dest['lon'] = Decimal(l +math.atan2(math.sin(t)*math.sin(d)*math.cos(p),cos(d)-math.sin(p)*math.sin(dest['lat'])))
                return dest



