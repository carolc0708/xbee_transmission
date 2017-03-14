# xbee_transmission

STEP 1: Raspberry pi should be set up with static IP address for pietty to connect.  
STEP 2: Open a terminal, execute `$ roscore`.  
STEP 3: Open the second terminal, and do the following.
```
$ cd catkin_ws
$ source ./devel/setup.bash # every time after file content is revised 
$ rosrun xbee_transmission store_data_server.py
```
STEP 4: Open the third terminal, and do the following.
```
$ cd catkin_ws
$ source ./devel/setup.bash # every time after file content is revised 
$ rosrun xbee_transmission store_data_client.py 5.666 7.888 # assign a waypoint coordinate for it
```
If request is sent out, you will get the message:
```
[Request waypoint] 5.66600 7.88800
```
STEP 5: Wait for about 10 seconds, you will recieve the following if the data is successfully collected.
```
[Response] 1 # response 1 if succeed
```

> If you do not receive response after 10 seconds, it probably fails due to unexpected error.

STEP 6: Check if the data is collected and with correct content.
```
$ cd ~/catkin_ws/src/xbee_transmission/file/5.666_7.888$
$ ls
```
You will see the following result. Check the content using `$ vim` command.
```
1.csv  2.csv  3.csv  4.csv  5.csv  6.csv  7.csv
```
