#!/usr/bin/env python

from xbee_transmission.srv import *
import rospy
import subprocess

def handle_receive_packet(req):
	
	s = subprocess.Popen(["python","/home/carol/catkin_ws/src/xbee_transmission/scripts/tx_with_arduino.py", str(req.day)],stdout=subprocess.PIPE).communicate()[0]
 
	#s = '{simulate_packet}'
	print '[from request number] %d [Returning receive packet] %s'%(req.day, s)
	return packetResponse(s)

def xbee_server():
	rospy.init_node('xbee_server')
	ser = rospy.Service('receive_packet', packet, handle_receive_packet)
	print 'Ready to receive packet.'
	rospy.spin()

if __name__ == '__main__':
	try:
		xbee_server()
	except rospy.ROSInterruptException:
		pass
