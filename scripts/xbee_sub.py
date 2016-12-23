#!/usr/bin/env python

#subscriber: the one that need the received data
#purpose: response that it has received the packets


import rospy
from std_msgs.msg import String

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def xbee_sub():
	rospy.init_node('xbee_sub', anonymous=True)
	rospy.Subscriber('chatter', String, callback)

	rospy.spin()

if __name__ == '__main__':
	xbee_sub()
