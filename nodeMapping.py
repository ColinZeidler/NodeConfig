import requests, json

JSON_PORT = 9090
jsonurl = "http://localhost:{port}".format(port=JSON_PORT)


def createDistMap(systems, wlanIP='127.0.0.1'):
	"""
	takes an array for system ips
	returns a map of hop distance and ips
	{3: ['10.1.1.1', '10.1.2.1'],
	2: ['10.2.1.2']}
	"""
	distMap = {}
	r = requests.get(jsonurl)
	r.raise_for_status()

	j = json.loads(r.text)['routes']
	for node in j:
		if node['destination'] in systems:
			try:
				distMap[node['metric']].append(node['destination'])
			except KeyError:
				distMap[node['metric']] = [node['destination']]
			print "{ip} is {dist} hops away".format(ip=node['destination'], dist=node['metric'])

	# we should also check what our wan0 address is
	if 'localhost' in systems or '127.0.0.1' in systems:
		distMap[0] = ['localhost']
	elif wlanIP in systems:
		distMap[0] = [wlanIP]
	
	return distMap


def createTopologyMap():
	topo_list = []
	r = requests.get(jsonurl)
	r.raise_for_status()
	
	j = json.loads(r.text)['topology']
	for item in j:
		connection = {}
		connection['source'] = item['lastHopIP']
		connection['target'] = item['destinationIP']
		topo_list.append(connection)

	return topo_list
