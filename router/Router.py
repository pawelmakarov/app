class Router(object):
	def __init__(self, route_strings):
		self.route_strings = route_strings

	def route_for_uri(self, uri):
		for route in self.route_strings:
			if route.matches_uri(uri):
				return route
		raise ValueError('No route has been found!')
