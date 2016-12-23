#!/usr/bin/env python

import sys
import rospy
from xbee_transmission.srv import *

def xbee_client(s):
	rospy.init_node('xbee_client')
	rospy.wait_for_service('receive_packet')
	client = rospy.ServiceProxy('receive_packet', packet)

	#s = 'give me received packets'
	resp1 = client(s)
	return resp1.response
	#print '[Requesting Query] %s'%s
	#print '[receive packet] %s'%resp1.response

#def usage():
#	return '[usage] %s'%sys.argv[0]

if __name__ == '__main__':
	try:
		if len(sys.argv) == 2:
			day = int(sys.argv[1])
			print '[Requesting] %d'%day
			print '[Respnse] %s'%xbee_client(day)
		else:
			print 'invalid input'
	except rospy.ROSInterruptException:
		pass
