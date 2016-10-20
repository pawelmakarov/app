from os.path import dirname

class Properties(object):
	def readFromFile(self):
		routes_lst = []

		fname = dirname(__file__) + '/routes.conf'
		fname = fname.replace('router', 'conf')

		with open(fname, 'r') as stream:
			for line in stream:
				routes_lst.append(line.rstrip('\n'))
		return routes_lst
