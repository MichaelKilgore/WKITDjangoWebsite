

class Cities():
	cities = []
	def __init__(self):
		file = open('cities.txt', 'r')
		lines = file.readlines()

		for line in lines:
			cities.append(line)

