# /usr/bin/python

from xbee.zigbee import ZigBee
import serial
import time
import sys


# packet resend verification function
def packet_verification(rp):
	resend_packet_no = []
	for i in range(len(rp)):
		if not rp[i] or ((ord(rp[i]['rf_data'][0])-48) * 10 + (ord(rp[i]['rf_data'][1])-48)) != i+1:
			#print 'resend packet:'
			#print i
			#print '-----------------'
			resend_packet_no.append(i)
			i += 1
			continue
	return resend_packet_no

		
	
# for disabling 16-bit addr.
UNKNOWN = '\xff\xfe'

NUM_OF_DEST = 1
# the addr. of arduino xbee
DEST = '\x00\x13\xa2\x00\x40\x69\x4e\x28'


# open a serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Create XBee Serial 2 object
xbee = ZigBee(ser, escaped=True)

test = sys.argv[1]
#print test

#RECEIVED_PACKET = []
# What times you want to run?
RUN_TIMES = 1
MAX_PACKET_CNT = 48
RECEIVED_PACKET = [[0 for x in range(MAX_PACKET_CNT)] for y in range(RUN_TIMES)]

#for i in range(RUN_TIMES):
	#RECEIVED_PACKET.append([])

#skip check if no file
skip_check = 0

# depend on # of day (data i)
for i in range(RUN_TIMES):

	# send tx packet to request all data of DAY i 
	xbee.tx(dest_addr_long=DEST, dest_addr=UNKNOWN, data='data'+ str(test) +'00') #test2 str(i+1)

	#create a lock here
	expired_time = 5
	t0 = time.clock()
	#packet_cnt = 0
        
	#receive data one-by-one before time expired
	while(time.clock() - t0 < expired_time):
		time.sleep(.01)
		response = xbee.wait_read_frame()
		print response		
		if response['id'] == 'rx' :
			if response['rf_data'] == 'end\x00\x00\x00\x00\x00\x00\x00':
				break
			elif response['rf_data'] == 'nofile\x00\x00\x00\x00':
				skip_check = 1
				break
			else:
				packet_ind = (ord(response['rf_data'][0])-48) * 10 + (ord(response['rf_data'][1])-48)
				#print packet_ind
				if packet_ind > 0 and packet_ind <= 48:
					RECEIVED_PACKET[i][packet_ind-1] = response 
				
	#verify the content and request for re-send if needed
	if skip_check == 0:

		resend_packet_no = packet_verification(RECEIVED_PACKET[i])
		resend_packet_cnt = len(resend_packet_no)
  
		if resend_packet_cnt != 0 : 
			# send tx packet to request for particular data of DAY i
			for j in range(resend_packet_cnt):
				k = resend_packet_no[j]
				# handling request context
				if k+1 < 10:
					data_='data' + str(test) + '0' + str(k+1) #str(i+1)
				else:
					data_='data' + str(test) + str(k+1)
				#print data_
				xbee.tx(dest_addr_long=DEST, dest_addr=UNKNOWN, data=data_) # not sure
			
				#receive the data before time expired
				expired_time = 2 #need check
				t0 = time.clock()
        			while(time.clock() - t0 < expired_time):
               				time.sleep(.01)
                			response = xbee.wait_read_frame()
					#print response
                			if response['id'] == 'rx' :
                       				RECEIVED_PACKET[i][k] = response
						break


                             		

#print out the received packet content
"""
Python can directly print array like [[...], [...], [...], ...].
If your 2-D array RECEIVED_PACKET have different columns length, 
you can use "range(len(RECEIVED_PACKET[i]))" to control second layer for loop.
"""
print('==============================================================================================================================================================')
print('\n\n[DAY'+ test +'] received:')
for item in RECEIVED_PACKET[0]:
	if not item: # for no file case
		print 'nothing'
		break
	elif item['rf_data'][2:] != '00000000000000':
		print(item)

ser.close()
