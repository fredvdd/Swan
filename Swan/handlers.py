from Actors.keywords import *
from Util.exceptions import *
from Actors.Device.file import File
from Swan.static import log
from Swan.fields import *
from BaseHTTPServer import BaseHTTPRequestHandler
import json
import mimetypes as mt

class Handler(StaticActor):
	
	def birth(self):
		pass
	
	def respond(self, method, specifier, request):
		response = request.start_response()
		if method == 'OPTIONS':
			self.options(specifier, request, response)
		handle_name = "%s_%s" % (method.lower(), specifier) if specifier else method.lower()
		handle_method = getattr(self, handle_name)
		handle_method(request, response)
	
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
		connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
		request.set_status(200).set_headers([
			("Content-type", "text/xml"),
			("Connection", connection),
			("Content-length", len(content))
		]).end_headers().respond("%s" % content).done()

class DefaultHandler(Handler):
	
	def do404(self, request, response):
		path = request.path
		log.debug(self, "Resource for %s not found" % path)
		response.send_error(404, "Resource at %s could not be found" % path)
	
	head = get = put = post = delete = do404

class FileHandler(Handler):

	def birth(self, root, workers):
		self.root = root
		self.workers = workers

	def get(self, request, response):
		path = request.params['path']
		filepath = self.root+path
		
		filename = filepath.split('/')[-1]
		content_type = mt.guess_type(filename)[0]
		
		if not content_type and filename.split('.'):
			filepath += 'index.html' if filepath[-1]=='/' else '/index.html'
			content_type = 'text/html'
			
		log.debug(self, "request for %s on %s" % (filepath, request.socket))
		callback('send_get_response', one(self.workers).read(filepath), request, response, content_type)

			
	def send_get_response(self, content, request, response, content_type):
		path = request.params['path']
		if content:
			connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
			log.debug(self, "responding with content of %s for %s" % (path, request.socket))
			response.set_status(200).set_headers([
				("Content-type", content_type),
			 	("Connection", connection),
				("Content-length", len(content))
			]).end_headers().send("%s" % content).done()
			log.debug(self, "finished handling %s for %s" % (path, request.socket))
		else:
			log.error(self, "couldn't find %s for %s" % (path, request.socket))
			response.send_error(404, "Resource at %s could not be found" % path)
			
	def head(self, request):
		pass
	
class DatabaseHandler(Handler):
	
	def birth(self, workers):
		self.workers = workers
		clazz = self.__class__
		self.table = clazz.__name__
		self.fields = [(x,y) for x,y in clazz.__dict__.iteritems() if isinstance(y, Field)]
		self.fieldnames = [x for x,y in self.fields]
		self.fieldstring = reduce(lambda a,b: "%s, %s" % (a,b), self.fieldnames)
		
	def get(self, request, response):
		rows = one(self.workers).execute("SELECT %s FROM %s" % (self.fieldstring, self.table))
		dicts = [dict(zip(self.fieldnames, row)) for row in rows]
		enc = json.dumps({self.table : dicts})
		connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
		response.set_status(200).set_headers([
			("Content-type", "application/json"),
		 	("Connection", connection),
			("Content-length", len(enc))
		]).end_headers().send(enc).done()
		
	def get_detail(self, request, response):
		col, val = (request.params['col'], request.params['val'])
		sql = "SELECT %s FROM %s WHERE %s = ?" % (self.fieldstring, self.table, col)
		rows = one(self.workers).execute(sql, (val,))
		dicts = [dict(zip(self.fieldnames, row)) for row in rows]
		enc = json.dumps({self.table : dicts})
		connection = "close" if not request.headers.has_key('Connection') else request.headers['Connection']
		response.set_status(200).set_headers([
			("Content-type", "application/json"),
		 	("Connection", connection),
			("Content-length", len(enc))
		]).end_headers().send(enc).done()

	def put(self):
		pass
	
	def post(self):
		pass
		
	def delete(self):
		pass