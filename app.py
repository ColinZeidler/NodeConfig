from flask import Flask, request, render_template
from nodeMapping import createDistMap, createTopologyMap
from updateNodes import NodeConnection
import json, requests
app = Flask(__name__)

import socket
import fcntl
import struct
def getIP(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(), 0x8915, struct.pack('256s', ifname[:15])
	)[20:24])

wlanIP = getIP('wlan0')


@app.route('/nodes')
def node_list():
	'''
	returns a list of node objects:
	{'id': 'ip','name': 'hostname'}
	'''
	olsr_host_f = "/var/run/hosts_olsr"

	topo_nodes = {}
	r = requests.get("http://localhost:9090")
	j = json.loads(r.text)['topology']
	for n in j:
		topo_nodes[n['destinationIP']] = n['destinationIP']
		topo_nodes[n['lastHopIP']] = n['lastHopIP']
	
	nodes = {}
	with open(olsr_host_f, 'r') as f:
		for line in f:
			item = {}
			line = line.strip().split("#")[0]
			if line != '' and 'mid1.' not in line and 'dtdlink.' not in line:
				line = line.split()
				if line[1] != 'localhost':
					nodes[line[0]] = line[1]

	for k in topo_nodes.keys():
		try:
			topo_nodes[k] = nodes[k]
		except KeyError:
			pass # nothing to do

	nodes = []
	for k in topo_nodes.keys():
		item = {}
		item['id'] = k
		item['name'] = topo_nodes[k]
		nodes.append(item)

	return json.dumps(nodes)

@app.route('/topology')
def topo_map():
	'''
	returns a list of connection objects
	{'source': 'ip', 'target': 'ip'}
	'''
	return json.dumps(createTopologyMap())


@app.route('/configure', methods=['POST'])
def configure_nodes():
	'''
	systems sould be an ip, with an associated username and password
	{'127.0.0.1': {'username': 'test', 'password': 'testing'}}
	'''
	new_options = request.form['options']
	new_options = json.loads(new_options)
	rpi_options = {
		"data[NetworkSetting][wan_dns2]": new_options['dns2'], 
		"data[NetworkSetting][wifi_channel]": new_options['channel'], 
		"data[NetworkSetting][ntp_server]": new_options['ntp'], 
		"data[NetworkSetting][mesh_olsrd_secure]": new_options['secure_enable'],
		"data[NetworkSetting][wan_dns1]": new_options['dns2'], 
		"data[NetworkSetting][wifi_ssid]": new_options['ssid'], 
		"data[NetworkSetting][mesh_olsrd_secure_key]": new_options['secure_key']
		}
	systems_d = request.form['systems']
	systems_d = json.loads(systems_d)

	systems = systems_d.keys()

	systems = createDistMap(systems, wlanIP)
	dist = max (systems.keys())
	while dist >= 0:
		try:
			for sys in systems[dist]:
				node = NodeConnection(sys)
				node.login(systems_d[sys]['username'], systems_d[sys]['password'])
				node.updateSettings(rpi_options)
				node.reboot()
				# TODO handle connection errors
		except KeyError:
			# no need to do anything
			pass
		dist -= 1
	return "success"


@app.route('/')
def index_page():
	return render_template("index.html")


if __name__ == "__main__":
	app.run('0.0.0.0')
