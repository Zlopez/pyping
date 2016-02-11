#!/usr/bin/env python3

#Extended ping with new logging data to csv file for graphs.
#Author: Michal Konecny

import subprocess
import re
import time
import datetime
import signal
import sys

#Global constants
CSV_FILE="graph.csv"
IP_ADDRESS="8.8.8.8"

#First run ping

def runPing():
	time_pattern = re.compile('(?<=time=)[\d\.]+')
	timeout = []
	timeout_count = 0
	ping_counter = 0
	time_ping_sum = 0.0
	max_ping = 0.0
	min_ping = 9999.0
	timeouts_length = 0

	prepareCSVFile()
	try:
		while 1:
			time.sleep(1)
			child = subprocess.Popen(["ping", "-c1", IP_ADDRESS],stdout=subprocess.PIPE,universal_newlines=True)
			ping_counter += 1
			ping = child.communicate()[0]
			now = (str(datetime.datetime.now()).split('.')[0])

			#Check if we received the ping back
			if (child.returncode == 0):
				if len(timeout) > 0 and timeout[0] == timeout[1]:
					timeout[1] = now
					print("Timeout from: " + timeout[0] + " to: " + timeout[1])
					timeout = []
					timeout_count += 1
				match = re.search(time_pattern,ping)
				time_ping = float(match.group(0))
				time_ping_sum += time_ping
				# save max and min values
				if max_ping < time_ping:
					max_ping = time_ping
				if min_ping > time_ping:
					min_ping = time_ping
			else:
				time_ping = 0.0
				timeouts_length += 1
				if not timeout:
					timeout = [now,now]

			saveLatencyToFile(now + ',' + str(time_ping))
			time_ping = None
	except (SystemExit,KeyboardInterrupt):
		printStatistics(timeout_count, timeouts_length, time_ping_sum, ping_counter, max_ping, min_ping)

#Just erase content of file
def prepareCSVFile():
	f = open(CSV_FILE,'w')
	f.write('')
	f.close()

#Append one new line to CSV file
def saveLatencyToFile(string):
	f = open(CSV_FILE,'a')
	f.write(string + '\n')
	f.close()

#Print statistics to stdout
def printStatistics(timeout_count, timeouts_length, time_ping_sum, ping_counter, max_ping, min_ping):
		print("--------------------------------------------------")
		print("Number of timeouts: " + str(timeout_count))
		print("Time down: " + str(timeouts_length))
		print("Average latency: " + str("{0:.2f}".format(time_ping_sum/ping_counter)))
		print("Max latency: " + str(max_ping))
		print("Min latency: " + str(min_ping))

#Handle SIGTERM signal
def sigterm_handler(_signo, _stack_frame):
	sys.exit(0)

if __name__=='__main__':
	signal.signal(signal.SIGTERM, sigterm_handler)
	runPing()
