import socket
import urllib
import contextlib
import sys
import os

try:
	from logging import getLogger, ERROR
	getLogger('scapy.runtime').setLevel(ERROR)
	from scapy.all import *
except ImportError:
	print '[!] Error: Failed to Import Scapy'
	userChoice = raw_input('[*] Attempt to Auto-Install Scapy? [y/N] ').strip().lower()
	if userChoice[0] == 'y':
		print '[*] Attempting Auto-Install via Pip... ',; sys.stdout.flush()
		try:
			import pip
			pip.main(['install', '-q', 'scapy'])
			from scapy.all import *
			print '[DONE]'
		except Exception:
			print '[FAIL]'
			sys.exit(1)
	else:
		sys.exit(1)

class fingerPrinter(object):
	def __init__(self, servOpt=False, iface='eth0'):
		self.servOpt = servOpt
		self.sniffOpt = not self.servOpt
		self.iface = iface
		self.uaDict = self.getAgents()
	def getAgents(self):
		print '[*] Building User-agent Dictionary... ',; sys.stdout.flush()
		if not os.path.isfile('/usr/share/uafp/strings.py'):
			try:
				if not os.path.isdir('/usr/share/uafp'): os.makedirs('/usr/share/uafp')
				urllib.urlretrieve('http://raw.githubusercontent.com/TheDefalt/general/master/uafp/strings.py', '/usr/share/uafp/strings.py')
				with open('/usr/share/uafp/strings.py') as dictFile:
					exec dictFile #You may be wondering what code is being executed here. Good on you for being so paranoid! See the URL or filepath above to see it!
				print '[DONE]'
				return userAgents
			except Exception:
				print '[FAIL]'
				sys.exit(1)
		else:
			try:
				with open('/usr/share/uafp/strings.py', 'r+') as dictFile, contextlib.closing(urllib.urlopen('http://raw.githubusercontent.com/TheDefalt/general/master/uafp/strings.py')) as remoteFile:
					localVerNum = dictFile.readline()
					remoteVerNum = remoteFile.readline()
					if localVerNum != remoteVerNum:
						dictFile.seek(0)
						dictFile.write('%s\n' %(remoteVerNum))
						dictFile.truncate()
						dictFile.write(remoteFile.read())
						dictFile.seek(0)
					exec dictFile.read()
					print '[DONE]'
					return userAgents
			except Exception:
				print '[FAIL]'
				sys.exit(1)

test = fingerPrinter()
print test.uaDict
