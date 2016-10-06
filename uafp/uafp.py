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
	def __init__(self, servOpt=False, sniffOpt=True, iface='eth0', target=False, html=False):
		self.servOpt = servOpt
		self.sniffOpt = sniffOpt
		self.iface = iface
		self.uaDict = self.getAgents()
		self.target = target
		self.html = loadSite(html)
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
	def loadSite(self, siteFile):
		if not not siteFile:
			with open(siteFile, 'r') as file:
				return file.read()
		else:
			return "<html>\n<body>\n<h1>This is a UAFP Demo Site!</h1>\n(This is the default site)\n</body>\n</html>"
	def parseRequest(self, httpReq):
		return httpReq.split("User-Agent:")[1].split('\n')[1].strip() #Get only the user-agent string out of an HTTP GET request
	def serverOperation(self):
		servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		servSock.bind(('0.0.0.0', 80))
`		s.listen(5)
		loopStatus = True
		while loopStatus:
			conn, addr = s.accept()
			if not not self.target:
				if addr[0] == self.target:
					httpGET = conn.accept(1024)
					conn.send('HTTP/1.0 200 OK\n')
					conn.send('Content-Type: text/html\n\n')
					conn.send(self.html)
					conn.close()
					return httpGET
				else:
					conn.accept(1024)
					conn.send('HTTP/1.0 401 Unauthorized\n')
					conn.close()
