from Actors.keywords import *
from Actors.Device.file import File
from Manager.managerlog import log
from BaseHTTPServer import BaseHTTPRequestHandler
import time

class Handler(StaticActor):
	
	def birth(self):
		pass
	
	def respond(self, method, specifier, request):
		self.request = request
		handle_name = "%s_%s" % (method.lower(), specifier) if specifier else method.lower()
		handle_method = getattr(self, handle_name)
		handle_method(request)
	
class EchoHandler(Handler):
	
	def get(self, request):
		print "Echoing %s" % request
		request.respond("Echoing GET request with headers %s" % request.headers)
		request.done()

class FileHandler(Handler):

	def birth(self, root):
		self.root = root
		
	def get(self, request):
		path = request.params['path']
		log.debug(self, "request for %s on %s" % (path, request.socket))
		try:
			content_type = self.types[path.split('/')[-1].split('.')[-1]]
		except:
			content_type = 'text/html'
			
		content = File(self.root+path).read()
		if content:
			log.debug(self, "responding with content for %s on %s" % (path, request.socket))
			request.set_status(200) 
			request.set_header("Content-type", content_type)
			request.set_header("Connection", request.headers['Connection'])
			request.set_header("Content-length", len(content))
			request.end_headers()
			request.respond("%s" % content)
			log.debug(self, "finished handling %s on %s" % (path, request.socket))
			request.done()
		else:
			log.error(self, "couldn't find %s on %s" % (path, request.socket))
			request.respond_error(404, "Couldn't find file %s" % path)
			
	
	def http_error(self, code, message=None):
		name, more = BaseHTTPRequestHandler.responses[code]
		if not message:
			message = more

	types = {
		'html' : 'text/html',
		'jpg' : 'image/jpeg',
		'css' : 'text/css',
		'js' : 'application/javascript',
		'png' : 'image/png'
	}
