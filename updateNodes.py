from readSysList import getSystems
from htmlParsing import FormDefaultParser
from nodeMapping import createDistMap
import requests, json, sys

WEB_PORT = 8080
UNAME = 'admin'
PWORD = 'rzeidler'

class NodeConnection(object):
	def __init__(self, ip):
		self.ip = ip
		self.session = requests.Session()

		self.loginurl = "http://{ip}:{port}/hsmm-pi/users/login".format(ip=self.ip, port=WEB_PORT)
		self.rebooturl = "http://{ip}:{port}/hsmm-pi/system".format(ip=self.ip, port=WEB_PORT)
		self.settingsurl = "http://{ip}:{port}/hsmm-pi/network_settings/edit/1".format(ip=self.ip, port=WEB_PORT)

	def login(self, username, password):
		data = {"data[User][username]": username,
                "data[User][password]": password}
		print "Logging in"
		r = self.session.post(self.loginurl, data = data)

		r.raise_for_status()
		print "Logged into {ip} successfully".format(ip=self.ip)

	def updateSettings(self, newSettingMap):
		# read old settings
		parser = FormDefaultParser()
		print "Reading default settings"
		r = self.session.get(self.settingsurl)
		r.raise_for_status()
		print "Successfully read defaults"

		parser.feed(r.text)
		default_settings = parser.form_defaults_map
		# apply changes 
		default_settings.update(newSettingMap)
		# post in settings
		print "Applying new settings"
		r = self.session.post(self.settingsurl, data = default_settings)
		r.raise_for_status()
		print "Successfully updated settings"

	def writeDefaultSettings(self, filename):
		r = self.session.get(self.settingsurl)
		r.raise_for_status()

		parser = FormDefaultParser()
		parser.feed(r.text)
		jdata = json.dumps(parser.form_defaults_map)

		with open(filename, "w") as f:
			f.write(jdata)

	def reboot(self):
		print "Rebooting system"
		r = self.session.get(self.rebooturl)

		r.raise_for_status()
		print "Reboot request successful, system will reboot in 2 minutes"


if __name__ == "__main__":
	jsonFile = sys.argv[1]
	with open(jsonFile, "r") as f:
		jsonSettings = f.read()
	newSettings = json.loads(jsonSettings)
	systems = getSystems()

	systems = createDistMap(systems)
	dist = max(systems.keys())
	print systems
	while dist >= 0:
		try:
			for sys in systems[dist]:
				print "connecting to {}".format(sys)
				node = NodeConnection(sys)
				node.login(UNAME, PWORD)
				#node.writeDefaultSettings("defaults.json")
				node.updateSettings(newSettings)
				node.reboot()
		except KeyError:
			print "No systems {dist} hops away".format(dist=dist)
		dist -= 1
