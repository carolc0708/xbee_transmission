#!/usr/bin/env python

# publisher: the xbee port that receive data
# purpose: send the received packets from Arduino to its subscriber

import rospy
from std_msgs.msg import String
import subprocess

def xbee_pub():
	pub = rospy.Publisher('chatter', String, queue_size=10)
	rospy.init_node('xbee_pub', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		result = subprocess.Popen(["python","/home/carol/catkin_ws/src/xbee_transmission/scripts/tx_with_arduino.py"],stdout=subprocess.PIPE).communicate()[0]
		rospy.loginfo(result)
		pub.publish(result)
		rate.sleep()


if __name__ == '__main__':
	try:
		xbee_pub()
	except rospy.ROSInterruptException:
		pass
