from wsgiref.simple_server import make_server
from jinja2 import Environment, PackageLoader
from cgi import parse_qs
from Cookie import SimpleCookie
from collections import OrderedDict
from router.Router import Router
from router.Route import Route
from router.Properties import Properties

env = Environment(loader=PackageLoader('templates', ''))

def application(environ, start_response):
	template = find_template(environ.get('PATH_INFO', ''))
	headers = []
	content = {}
	http_params = {}

	if template != '404.html': #favicon.ico
		content['counter'] = set_cookies(environ, headers)

	if environ.get('REQUEST_METHOD') == 'GET':
		http_params = parse_qs(environ.get('QUERY_STRING', ''))

	if environ['REQUEST_METHOD'] == 'POST':
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0

		request_body = environ['wsgi.input'].read(request_body_size)
		http_params = parse_qs(request_body)
		
	headers.extend([('Content-type', 'text/html; charset=utf-8')])
	start_response('200 OK', headers)

	content['http_params'] = OrderedDict(sorted(http_params.items()))
	template = env.get_template(template)
	print '{0} content'. format(content)
	return [template.render(content).encode('utf-8')]

def set_cookies(environ, headers):
	cookies = SimpleCookie()
	cookie_name = 'page_visits'
	value = 1

	if environ.get('HTTP_COOKIE'):
		cookies = SimpleCookie(environ['HTTP_COOKIE'])

	if cookie_name in cookies:
		value = int(cookies[cookie_name].value) + value

	cookies[cookie_name] = value
	headers.extend(("set-cookie", morsel.OutputString()) for morsel in cookies.values())
	return value

def find_template(uri):
	router = Router(get_router())
	route = None

	try:
		route = router.route_for_uri(uri)
	except ValueError, message:
		print message 
		return '404.html'
	return route.template

def get_router():
	routes_config = Properties().readFromFile()
	routes = []

	for route in routes_config:
		routes.append(Route(route))
	return routes

if __name__ == '__main__':
	httpd = make_server('localhost', 8000, application)
	httpd.serve_forever()
