#! /usr/bin/python

import socket
import sys

if len(sys.argv) < 4:
	print 'usage: ./scan.py [TARGET] [START PORT] [STOP PORT]'
	sys.exit(1)

rhost = sys.argv[1]
start = sys.argv[2]
stop = sys.argv[3]

def scan_port(num):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = s.connect_ex((rhost, num))
		s.close()
		if result == 0:
			return True
		else:
			return False
	except:
		return False

print 'starting scan...\n'

for i in range(int(start), int(stop)+1):
	if scan_port(i):
		print 'port %s: open' %(i)

print '\nscan complete'
