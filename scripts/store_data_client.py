#!/usr/bin/env python

import sys
import rospy
from xbee_transmission.srv import *

import os.path
import subprocess

def store_data_client(x,y):
	rospy.init_node('store_data_client')
	rospy.wait_for_service('store_data_service')
	client = rospy.ServiceProxy('store_data_service', store_data)
	
	resp = client(x,y)
	return resp.response

if __name__ == '__main__':
	try:
		if len(sys.argv) == 3:
			x = float(sys.argv[1])
			y = float(sys.argv[2])
			# delete directory if already exist
			file_path = '/home/carol/catkin_ws/src/xbee_transmission/file/'+str(x)+'_'+str(y)
			if os.path.exists(file_path):
				subprocess.Popen(['rm', '-r', file_path+'/'],stdout=subprocess.PIPE) 
			print '[Request waypoint] %.5f %.5f'%(x,y)
			print '[Response] %d'%store_data_client(x,y)
		else:
			print 'invalid input'
	
	except rospy.ROSInterruptException:
		pass
