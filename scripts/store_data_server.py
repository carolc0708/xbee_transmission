#!/usr/bin/env python

from xbee_transmission.srv import *
import rospy
import subprocess

# for csv write file
import csv
import os
import sys
import yaml

def split_data(dict_string):
	temp = dict_string.split('\n')
	
	result = []
	
	# convert string back to dict
	for i in range(1, len(temp)-1):
		# transform to dict
		d = yaml.load(temp[i])
		# string preprocess
		d = d['rf_data'].split('\\')[0]
		d = d[2:]
		if d != '':
			result.append(d.split(','))
		
	return result
		


def handle_store_data(req):
	 # create the sub directory first
	file_path = '/home/carol/catkin_ws/src/xbee_transmission/file' + '/' + str(req.x) + '_' + str(req.y)
	os.mkdir(file_path,0777)

	day_cnt = 7
	data_miss = 0
	for i in range(day_cnt):
		# write to file
		os.chdir(file_path)

		if os.getcwd() != file_path:
			print "EEROR: the file path incorrect."
			msg = 2
			sys.exit()
			return store_dataResponse(msg)

		file = open(file_path + '/' + str(i+1) + '.csv', 'w')
		csvCursor = csv.writer(file)	

		# write header to csv file
		#csvHeader = ['timestamp', 'machine_id', 'user_id', 'boxState']
		#csvCursor.writerow(csvHeader)
		result = subprocess.Popen(["python","/home/carol/catkin_ws/src/xbee_transmission/scripts/tx_with_arduino.py", str(i+1)],stdout=subprocess.PIPE).communicate()[0]
		if(result.split('\n')[1] != 'nothing'):
			# record data miss
			data_miss += 1
			# split data
			data = split_data(result)
			# write row
			csvCursor.writerows(data)

		file.close()
	if data_miss == day_cnt:
		# inform to provide another waypoint 
		msg = 3 
		# delete current folder
		if os.path.exists(file_path):
                	subprocess.Popen(['rm', '-r', file_path+'/'],stdout=subprocess.PIPE)

	else:
		msg = 1
	
	return store_dataResponse(msg)

def store_data_server():
	rospy.init_node('store_data_server')
	ser = rospy.Service('store_data_service', store_data, handle_store_data)
	print 'Ready to handle data storing'
	rospy.spin()

if __name__ == '__main__':
	try:
		store_data_server()
	except rospy.ROSInterruptException:
		pass
