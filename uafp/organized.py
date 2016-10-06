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

def fingerPrinter(object):
	def __init__(self, servOpt=False, iface='eth0', target=False, siteFile=False):
		self.servOpt = servOpt
		self.sniffOpt = not self.servOpt
		self.iface = iface
		self.userAgents = self.getAgents()
		self.siteCode = self.loadSite(siteFile)
	def getAgents(self):
		if not os.path.isfile('/usr/share/uafp/strings.py'):
			if not os.path.isdir('usr/share/uafp'):
				os.makedirs('/usr/share/uafp')
			urllib.urlretrieve('http://raw.githubusercontent.com/TheDefalt/general/master/uafp/strings.py', '/usr/share/uafp/strings.py')
			with open('/usr/share/uafp/strings.py') as dictFile:
					exec dictFile #You may be wondering what code is being executed here. Good on you for being so paranoid! See the URL or filepath above to see it!
			return userAgents
		else:
			with open('/usr/share/uafp/strings.py', 'r+') as dictFile, contextlib.closing(urllib.urlopen('http://raw.githubusercontent.com/TheDefalt/general/master/uafp/strings.py')) as remoteFile:
				if dictFile.readline() != remoteFile.readline():
					dictFile.seek(0)
					dictFile.write('%s\n' %(remoteVerNum))
					dictFile.truncate()
					dictFile.write(remoteFile.read())
					dictFile.seek(0)
				exec dictFile.read()
				return userAgents
	def parseRequest(self, httpReq):
		return httpReq.split("User-Agent:")[1].split('\n')[1].strip() #Get only the user-agent string out of an HTTP GET request
	def loadSite(self, siteFile):
		if not not siteFile:
			with open(siteFile, 'r') as file:
				return file.read()
		else:
			return "<html>\n<body>\n<h1>This is a UAFP Demo Site!</h1>\n(This is the default site)\n</body>\n</html>"
	
