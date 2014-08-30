#Ardupilot class for communication with APM2.6 via UART0
#Created 29/08/2014
#Gregory Brooks
#Based on ardupilot.py by Dr G Owen
#https://github.com/drgowen/ardupilot-sdk-python.git

import sys, serial, time, thread
import mavlinkv10 as mavlink
from pymavlink import mavutil

class ArduPilot:
	def __init__(self, port, baud, verbose):
		self.verbose = verbose
		self.vprint ("Connecting...")
		self.mav = mavutil.mavlink_connection(port, baud, autoreconnect = True)	#set up serial connection to autopilot
		
		self.vprint("Waiting for first heartbeat")
		self.mav.wait_heartbeat()
		self.lastSentHeartbeat = time.time()

		self.vprint("Starting message handler thread")
		thread.start_new_thread(self.mavMsgHandler, (self.mav,)) #comma because tuple argument

	#handle incoming messages
	def mavMsgHandler(self,m):	
		while True:
			msg = m.recv_msg()
			if msg is None or msg.get_type() == "BAD_DATA":
				time.sleep(0.01)
				continue
			#"enable data streams after startup - can't see another way of doing this"
			if msg.get_type() == "STATUSTEXT" and "START" in msg.text:
				self.vprint(msg.text)
				self.vprint("Enabling data streams...")
				self.setDataStreams(mavlink.MAV_DATA_STREAM_EXTRA1)
				self.setDataStreams(mavlink.MAV_DATA_STREAM_EXTENDED_STATUS)
				self.setDataStreams(mavlink.MAV_DATA_STREAM_EXTRA2)
				self.setDataStreams(mavlink.MAV_DATA_STREAM_POSITION)
			if "ACK" in msg.get_type():
				print msg

			
	def getLocation(self):
		while 'GPS_RAW_INT' not in self.mav.messages:#wait for GPS data
			time.sleep(1)
		gps = self.mav.messages['GPS_RAW_INT']
		nd = self.dictCopy(gps, ['fix_type', 'lat', 'lon' ])
		nd['lat'] = nd['lat'] / 10e6
		nd['lon'] = nd['lon'] / 10e6
		return nd
	def dictCopy(self, src, keys):
		newDict = {}
		for k in keys:
			newDict[k] = getattr(src,k)
		return newDict
		


	def vprint(self,str):	#print stuff if verbose is true
		if self.verbose:
			print str

