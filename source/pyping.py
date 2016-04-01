#!/usr/bin/env python3

#Timeout checker that uses ordinary ping command to check for any timeout. Also has the ability to plot graph.
#Author: Michal Konecny

import subprocess
import re
import time
import datetime
import signal
import sys
import argparse
import socket
import matplotlib.pyplot as plt

#Global variables
temp_file="/tmp/pyping.data"
ip_address="8.8.8.8"
debug=False
graph=""

#Parse arguments
def parseArguments():
  global debug
  global graph
  global ip_address

  parser = argparse.ArgumentParser(description='Timeout checker using ordinary ping.')
  parser.add_argument('-d',action='store_true',help='Show debug information.')
  parser.add_argument('-g',help='Path to file for graph plotting. If no file is specified, graph will not be plotted.')
  parser.add_argument('address',help='Address to check for timeouts.')
  args = parser.parse_args()
  if args.d:
    debug = True
    if debug:
      print ("DEBUG: Found argument -d. Printing debug informations.")
  if args.g:
    graph = args.g
    if debug:
      print ("DEBUG: Found argument -g. Graph will be printed to " + graph + ".")
  if args.address:
    try:
      socket.inet_aton(args.address)
      ip_address = args.address
      if debug:
        print ("DEBUG: Address found " + ip_address + ".")
    except socket.error:
      print ("Argument address is not valid.")
      exit(1)

#Plot graph to specified location


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

  #Create file only when graph will be plotted
  if graph:
    prepareCSVFile()
  try:
    if debug:
      print ("DEBUG: Waiting for timeouts.")
    while 1:
      time.sleep(1)
      child = subprocess.Popen(["ping", "-c1", ip_address],stdout=subprocess.PIPE,universal_newlines=True)
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
        if debug:
          print ("DEBUG: Ping value " + str(time_ping) + " ms.")
        time_ping_sum += time_ping
        # save max and min values
        if max_ping < time_ping:
          max_ping = time_ping
        if min_ping > time_ping:
          min_ping = time_ping
      else:
        if debug:
          print ("DEBUG: Timeout detected.")
        time_ping = 0.0
        timeouts_length += 1
        if not timeout:
          timeout = [now,now]

      #Print to temp file only if graph will be plotted
      if graph:
        saveLatencyToFile(now + ',' + str(time_ping))
      time_ping = None
  except (SystemExit,KeyboardInterrupt):
    if debug:
      print ("DEBUG: Script interrupted.")
    printStatistics(timeout_count, timeouts_length, time_ping_sum, ping_counter, max_ping, min_ping)

#Just erase content of file
def prepareCSVFile():
  if debug:
    print ("DEBUG: Creating temp file: " + temp_file +  ".")
  with open(temp_file,'w') as f:
    f.write('')

#Append one new line to CSV file
def saveLatencyToFile(string):
  with open(temp_file,'a') as f:
    f.write(string + '\n')

#Print statistics to stdout
def printStatistics(timeout_count, timeouts_length, time_ping_sum, ping_counter, max_ping, min_ping):
    if debug:
      print ("DEBUG: Printing statistics.")
    print("--------------------------------------------------")
    print("Number of timeouts: " + str(timeout_count))
    print("Time down: " + str(timeouts_length))
    if ping_counter > 0:
      print("Average latency: " + str("{0:.2f}".format(time_ping_sum/ping_counter)))
    else:
      print("Average latency: " + str("{0:.2f}".format(time_ping_sum)))
    print("Max latency: " + str(max_ping))
    print("Min latency: " + str(min_ping))

#Handle SIGTERM signal
def sigterm_handler(_signo, _stack_frame):
  if debug:
    print ("DEBUG: Script interrupted by signal.")
  printStatistics(timeout_count, timeouts_length, time_ping_sum, ping_counter, max_ping, min_ping)
  sys.exit(0)

if __name__=='__main__':
  parseArguments()
  signal.signal(signal.SIGTERM, sigterm_handler)
  runPing()
