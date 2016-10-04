import socket
import urllib
import sys
import os

try:
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
