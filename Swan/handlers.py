from Actors.keywords import *
from Util.exceptions import *
from Actors.Device.file import File
from Swan.static import log
from BaseHTTPServer import BaseHTTPRequestHandler
import time

class Handler(StaticActor):
	
	def birth(self):
		pass
	
	def respond(self, method, specifier, request):
		self.request = request
		if method == 'OPTIONS':
			self.options(specifier, request)
		handle_name = "%s_%s" % (method.lower(), specifier) if specifier else method.lower()
		handle_method = getattr(self, handle_name)
		handle_method(request)
	
	def options(self, specifier, request):
		print "OPTIONS for " + request.path
		pattern = "%s" if not specifier else "%s_" + specifier
		methods = ['get', 'put', 'delete', 'post', 'head']
		options = []
		for method in methods:
			if hasattr(self, pattern % method):
				options.append(method)
		content = reduce(lambda a,b: a+b, map(lambda x: "<method>%s</method>" % x, options))
		content = "<methods>" + content + "</methods>"
		log.debug(self, "OPTIONS for %s are %s" % (request.path, content))
		request.set_status(200)
		request.set_header("Content-type", "text/xml")
		connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
		request.set_header("Connection", connection)
		request.set_header("Content-length", len(content))
		request.end_headers()
		request.respond("%s" % content)
		request.done()

class DefaultHandler(Handler):
	
	def do404(self, request):
		path = request.path
		log.debug(self, "Resource for %s not found" % path)
		request.respond_error(404, "Resource at %s could not be found" % path)
	
	head = get = put = post = delete = do404

class FileHandler(Handler):

	def birth(self, root, workers):
		self.root = root
		self.workers = workers

	def get(self, request):
		path = request.params['path']
		try:
			content_type = self.types[path.split('/')[-1].split('.')[-1]]
		except:
			content_type = 'text/html'
		filepath = self.root+path
		log.debug(self, "request for %s on %s" % (path, request.socket))
		callback('send_get_response', one(self.workers).read(self.root+path), request, content_type)

			
	def send_get_response(self, content, request, content_type):
		path = request.params['path']
		if content:
			log.debug(self, "responding with content of %s for %s" % (path, request.socket))
			request.set_status(200) 
			request.set_header("Content-type", content_type)
			connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
			request.set_header("Connection", connection)
			request.set_header("Content-length", len(content))
			request.end_headers()
			request.respond("%s" % content)
			log.debug(self, "finished handling %s for %s" % (path, request.socket))
			request.done()
		else:
			log.error(self, "couldn't find %s for %s" % (path, request.socket))
			request.respond_error(404, "Resource at %s could not be found" % path)
			
	def head(self, request):
		pass

	types = {
		'html' : 'text/html',
		'jpg' : 'image/jpeg',
		'css' : 'text/css',
		'js' : 'application/javascript',
		'png' : 'image/png'
	}
	
class DatabaseHandler(Handler):
	
	def birth(self, workers):
		self.workers = workers
		
	def get(self, request):
		pass
		
	def put(self):
		pass
	
	def post(self):
		pass
		
	def delete(self):
		pass