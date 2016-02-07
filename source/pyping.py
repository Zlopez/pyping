#!/usr/bin/env python3

#Extended ping with new logging data to csv file for graphs.
#Author: Michal Konecny

import subprocess
import re
import time
import datetime

#First run ping

time_array = []
timestamp_array = []
time_pattern = re.compile('(?<=time=)[\d\.]+')
timeouts = []

while 1:
	time.sleep(1)
	child = subprocess.Popen(["ping", "-c1", "8.8.8.8"],stdout=subprocess.PIPE,universal_newlines=True)
	ping = child.communicate()[0]
	#print (ping.split('\n')[1])
	now = (str(datetime.datetime.now()).split('.')[0])

	#Check if we received the ping back
	if (child.returncode == 0):
		if len(timeouts) > 0 and timeouts[-1][0] == timeouts[-1][1]:
			timeouts[-1][1] = now
			print(timeouts[-1])
		match = re.search(time_pattern,ping)
		time_ping = float(match.group(0)) 
	else:
		time_ping = 0.0
		timeout = [now,now]
		timeouts.append(timeout)

	time_array.append(time_ping)
	timestamp_array.append(now)	
	#print (str(timestamp_array[-1]) +' '+ str(time_array[-1]))	
