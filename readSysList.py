
listFile = "misc/systemList.txt"

def getSystems():
	systems = []
	with open(listFile, "r") as f:
		for line in f:
			line = line.strip()
			if line[0] != '#':
				systems.append(line)

	return systems
