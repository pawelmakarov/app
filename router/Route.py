class Route(object):
	SLASH = '/'

	def __init__(self, route_str):
		self.route_str = route_str

	def matches_uri(self, uri):
		if self.get_index_page():
			return uri == Route.SLASH

		uri = uri.strip(Route.SLASH)
		route = self.route_str.strip(Route.SLASH)

		uri_lst = uri.split(Route.SLASH)
		route_lst = route.split(Route.SLASH)

		if len(uri_lst) != len(route_lst):
			return False

		for index, value in enumerate(route_lst):
			if value != uri_lst[index] and value[0] != '[':
				return False
		return True

	@property
	def template(self):
		template = ''

		if self.route_str == Route.SLASH:
			return 'news.html'

		template = self.route_str.strip(Route.SLASH)
		template = template.replace(Route.SLASH, '-')
		return template + '.html'

	def get_index_page(self):
		return self.route_str == '/'
