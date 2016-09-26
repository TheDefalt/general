#! /usr/bin/python

import sys
import socket
import requests

if len(sys.argv) != 3:
	print "usage: ./dirbrute.py [TARGET] [WORDLIST FILE]"
	sys.exit(1)

def checkHost(host):
	print 'getting protocol... ',; sys.stdout.flush()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		status = s.connect_ex((host, 80))
		s.close()
		if status == 0:
			print 'done: http\n'
			return 'http://'
		else:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			status = s.connect_ex((host, 443))
			s.close()
			if status == 0:
				print 'done: https\n'
				return 'https://'
			else:
				print 'fail'
				sys.exit(1)
	except:
		print 'fail'
		sys.exit(1)

def getWordlist(path):
	print 'reading wordlist... ',; sys.stdout.flush()
	try:
		with open(path) as file:
			wordlist = file.read().strip().split('\n')
			print 'done'
			return wordlist
	except:
		print 'fail'
		sys.exit(1)

rhost = sys.argv[1]
wordlist = getWordlist(sys.argv[2])
proto = checkHost(rhost)

def checkPath(uri):
	try:
		resp = requests.get("%s%s/%s" %(proto, rhost, uri)).status_code
		if resp == 200:
			return True
		else:
			return False
	except:
		return False

for i in wordlist:
	if checkPath(i):
		print 'path found: /%s' %(i)

print '\nscan complete'


