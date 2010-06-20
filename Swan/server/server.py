from Actors.keywords import *
from request import Request
from Swan.static import log
from itertools import cycle
from threading import Timer
from urlparse import urlparse

class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port, resources):
		log.debug(self, "SWAN Server starting...")
		self.resources = resources #resource dictionary pool
		self.handlers = []
		self.add_handler(100)
		self.sock = open_socket(port)
		self.accept()
		
	def accept(self):
		while 1:
			try:
				#message sending means server is interruptible for maintenance
				self.accept_connection() 
			except KeyboardInterrupt:
				self.sock.close()
				
	def accept_connection(self):
		log.debug(self, "Accepting connection")
		self.handler_cycle.next().handle(self.sock.accept())
		
	def add_handler(self, count = 1):
		self.handlers.extend([RequestHandler(self.resources) for n in range(0,count)])
		self.handler_cycle = cycle(self.handlers)

class RequestHandler(LocalActor):
	"""Reads request method, resource and headers"""

	def birth(self, registries):
		self.default_request_version = "HTTP/1.1" #needed for parse_request
		self.registries = registries
		
	def handle(self, sock):
		log.debug(self, "Conection from %s:%d" % sock.getpeername())
		rfile = sock.makefile('rb',-1)
		self.handle_request(sock, rfile)
	
	def handle_request(self, sock, rfile, wfile=None):
		#log.debug(self, "Handling connection from %s:%d" % sock.getpeername())
		try:
			sock.settimeout(2.0)
			raw_requestline = rfile.readline()
			sock.settimeout(None) #disable timeouts
			if not raw_requestline:
				log.debug(self, "No Request. Closing connection to %s:%d" % sock.getpeername())
				sock.close()
				log.debug(self, "\n****************\n\n****************")
				return
		
			request = raw_requestline.strip()
			log.debug(self, "Request: " + request)
		
			#get command, path, and request_version and headers
			command, request_path, http = raw_requestline.strip().split(' ')
			scheme, netloc, path, path_params, query, frag = urlparse(request_path)
		
			headers = {}
			headerline = rfile.readline()
			while not headerline.strip() == "":
				key, value = headerline.split(":",1)
				# print key," : ",value
				headers[key.strip()] = value.strip()
				headerline = rfile.readline()

			(responder_pool, specifier, params) = one(self.registries).lookup(path)
			#log.debug(self,"Responders: %s,\n Specifier: %s,\n Params: %s\n" % (responder_pool, specifier, params))
			request = Request(self, sock, rfile, wfile, command, path, headers, params, path_params, query, frag)
			handler = one(responder_pool)
			log.debug(self, "%s to %s" % (str(request), handler))
			handler.respond(request, specifier)
		except Exception as exc:
			log.warn(self, str(exc))
			

class Headers(dict):
		
	def __getitem__(self,key):
		dict.__getitem__(self, key.lower())
		
	def __setitem__(self,key,value):
		dict.__setitem__(self,key.lower(),value)