userAgents = {  'Windows': {'NT 6.3': '8.1', 'NT 6.2': '8', 'NT 6.1': '7', 'NT 6.0': 'Vista', 'NT 5.2': 'Server 2003/XP x64 Edition', 'NT 5.1': 'XP', 'NT 5.01': '2000 SP1', 'NT 5.0': '2000', 'NT 4.0': 'NT 4.0', '98': 'Millenium Edition/98', '9x 4.90': 'Millenium Edition', '95': '95', 'CE': 'CE'}}

for i in userAgents['Windows'].keys():
	print userAgents['Windows'][i]
