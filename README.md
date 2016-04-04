# pyping
Extented ping command written in python. 

##Features
* graph plotting
* summary statistics with average, max, min latency
* statistics with number of timeouts and summary time without connection

##Usage
pyping.py [-h] [-d] [-g G] address

address 
* Address to check for timeouts.

-h, --help  
* show this help message and exit
  
-d          
* Show debug information.
  
-g G        
* Path to file for graph plotting. If no file is specified, graph will not be plotted.
