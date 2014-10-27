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
                #Vectors to show the direction of each corner of the photo from the camera
                #right-handed, Z-down, X-front, Y-right
                #vector format (0,x,y,z) in metres (0 is used for Hamilton product)
                topleft = [math.tan(20.5), 0 - math.tan(27),1]
                topright = [math.tan(20.5),math.tan(27),1]
                bottomright = [0 - math.tan(20.5),math.tan(27),1]
                bottomleft = [0 - math.tan(20.5),0 - math.tan(27),1]

        def take(self):
                print "taking photo"
                command =  "raspistill " + "-n " + "-q " + self.quality + "-t " + "50 "
                loc = self.ap.getLocation()
                att = self.ap.getAttitude()
                alt = self.ap.getAltitude()
                bear = self.ap.getHeading()
                if self.exif['on/off'] == True:#if save exif data option enabled
                        if self.exif['location'] == True:
                                print loc
                                lat = self.ddtodms(loc['lat'])
                                lon = self.ddtodms(loc['lon'])#save lat/lon with photo
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
                        name = str(loc['lat']) + "_" + str(loc['lon'])#name as lat lon
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


        def Eul2quat(self, y,p,r):
                #convert extrinsic Eulerian angles (in yaw, pitch, roll order) to quaternion
                #http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/
                c1 = math.cos(y/2)
                c2 = math.cos(p/2)
                c3 = math.cos(r/2)
                s1 = math.sin(y/2)
                s2 = math.sin(p/2)
                s3 = math.sin(r/2)

                #rotations as quaternions
                yaw = [c1,0,0,s1]
                pitch = [c2,0,s2,0]
                roll = [c3, s3,0,0]
                #resultant quat
                quat = H(H(roll,pitch),yaw)
                
                return quat



                
        def H(self, a, b):
                #a and b have four elements
                #http://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
                #http://en.wikipedia.org/wiki/Quaternion#Hamilton_product
                
                w = a[0]
                x = a[1]
                y = a[2]
                z = a[3]
                p0 = b[0]
                p1 = b[1]
                p2 = b[2]
                p3 = b[3]

                row1 = w*p0 - x*p1 - y*p2 - z*p3
                row2 = w*p1 + x*p0 + y*p3 - z*p2
                row3 = w*p2 - x*p3 + y*p0 + z*p1
                row4 = w*p3 + x*p2 - y*p1 + z*p0

                ans = [row1, row2, row3, row4]
                return ans

        def rotate(self, v, R):
                #v is start vector, R is quaternion to apply
                P = [0,v[0],v[1],v[2]] #quaternion version of vector
                R1 = [R[0],0-R[1],0-R[2],0-R[3]]
                ans = H(H(R,P),R1)
                ans2 = [ans[1],ans[2],ans[3]]#convert back to vector
                return ans2

         def corners(p,l,t,d):
                #based on formula from http://www.movable-type.co.uk/scripts/latlong.html
                dest = {'lat': 0, 'lon': 0}
                dest['lat'] = Decimal(math.asin(math.sin(p)*math.cos(d)+math.cos(p)*math.sin(d)*math.cos(t)))
                dest['lon'] = Decimal(l +math.atan2(math.sin(t)*math.sin(d)*math.cos(p),cos(d)-math.sin(p)*math.sin(dest['lat'])))
                return dest
       
                
