
#UAV Camera System Code
#Created 22/8/2014
#Gregory Brooks
from __future__ import division
import apm, serial, time, photos, thread, subprocess

def process():
    global fifo
    global stop
    while 1:
                
                if not fifo:
                    
                    if stop == 1:
                            break
                    else:
                        continue
                t = time.time()
                loc = fifo.pop(0)
                att = fifo.pop(0)
                alt = fifo.pop(0)
                bear = fifo.pop(0)
                name = fifo.pop(0)
               
                Vectors = cam.getVectors(att, alt)
                
                if Vectors == [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]:
                        return
                cam.Perspective(name, Vectors)
#                cam.ndvi(name)
                #x = time.time() - t
                #print "Time taken: ", x
    stop = 2


#Ardupilot class settings
serport = '/dev/ttyAMA0' #USB0 for USB, AMA0 for GPIO
baud = 57600
verbose = True

ap=apm.ArduPilot(serport,baud, verbose)#instance of ArduPilot class

#while 1:
#       loc = ap.getLocation()
#       print loc
#       time.sleep(1)
cam = photos.camera(ap)
prev_time = time.time()
fifo = []
stop = 0
thread.start_new_thread(process,())
for x in range (0,300):
        
        while time.time() - prev_time < 2.5:
            #take photo every 2.5 seconds
            time.sleep(1)#speeds up consumer thread
            pass
        prev_time = time.time()
        loc, att, alt, bear, name = cam.take()
        fifo.append(loc)
        fifo.append (att)
        fifo.append (alt)
        fifo.append (bear)
        fifo.append (name)
        
        #testing code
        #print loc
        #print att
        #print bear
        #print ""
        #print"-----------------"
        #print ""
        #end of testing
stop = 1        
while stop !=2:
    time.sleep(7)
    pass
#too slow to do NDVI on raspi
#start = time.time()
#cmd = "python /root/Desktop/UAV/infrapix-mov/processNGB.py /root/dewarped/ /root/ndvi/ .1 .8 0"           
#subprocess.call(cmd, shell=True)
#print "NDVI time: ", time.time() - start

