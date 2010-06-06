from Actors.keywords import *
from Actors.Device.file import File
from Actors.threadlocal import thread_local
from Swan.static import log
import mimetypes as mt

class Handler(StaticActor):
	
	def birth(self):
		pass
	
	def respond(self, request, specifier):
		log.debug(self, "responding to %s" % request)
		response = request.start_response()
		method = request.method
		if method == 'OPTIONS':
			self.options(specifier, request, response)
			
		handle_name = "%s_%s" % (method.lower(), specifier) if specifier else method.lower()
		handle_method = thread_local.actor.state.get_method(handle_name)
		
		handle_method.func_globals.update(request=request, response=response)
		params = dict([(k,v) for (k,v) in request.params.iteritems() if not v == None])
		if method in ['PUT', 'POST']:
			params.update({'body':request.get_body()})
		handle_method(**params)
			
	
	def no_method(self, request, response, **superfluous):
		response.send_error(405, "The method %s is not supported on this resource" % request.method).send()
	
	#inspects handler for presence of methods and compiles response
	def options(self, specifier, request, response):
		log.debug(self,"OPTIONS for " + request.path)
		pattern = "%s" if not specifier else "%s_" + specifier
		methods = ['get', 'put', 'delete', 'post', 'head']
		options = [method for method in methods if hasattr(self, pattern % methods)]#[]
		content =  "<methods>" + reduce(lambda a,b: a+b, map(lambda x: "<method>%s</method>" % x, options)) + "</methods>"
		log.debug(self, "OPTIONS for %s are %s" % (request.path, content))
		response.with_status(200).with_content_type("text/xml").with_content("%s" % content).send()
	
	def __repr__(self):
		return "%s Handler" % (self.__class__.__name__)

class DefaultHandler(Handler):
	
	def do404(self):
		path = request.path
		log.debug(self, "Resource for %s not found" % path)
		response.send_error(404, "Resource at %s could not be found" % path).send()
	
	head = get = put = post = delete = do404

class FileHandler(Handler):

	def birth(self, root, workers):
		self.root = root
		self.workers = workers

	def get(self, path=None):
		filepath = self.root+path if path else self.root
		
		filename = filepath.split('/')[-1]
		content_type = mt.guess_type(filename)[0]
		
		if not content_type and filename.split('.'):
			filepath += 'index.html' if filepath[-1]=='/' else '/index.html'
			content_type = 'text/html'
			
		log.debug(self, "request for %s on %s" % (filepath, request.socket))
		callback('send_get_response', one(self.workers).read(filepath), request, response, content_type)

			
	def send_get_response(self, content, request, response, content_type):
		path = request.params.get('path','/')
		if content:
			log.debug(self, "responding with content of %s for %s" % (path, request.socket))
			response.with_status(200).with_content_type(content_type).with_content("%s" % content).send()
			log.debug(self, "finished handling %s for %s" % (path, request.socket))
		else:
			log.error(self, "couldn't find %s for %s" % (path, request.socket))
			response.send_error(404, "Resource at %s could not be found" % path).send()
	
	# def post(self, body, path=None):
	# 	filepath = self.root+path if path else self.root
			
			
class ExternalHandler(Handler):

	def birth(self, workers):
		self.workers = workers
		
	def get_connection(self, server):
		return one(self.workers).connect(server)