from Actors.keywords import *
from request import Request
from Swan.static import log
from itertools import cycle
from threading import Timer

class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port, resources):
		log.debug(self, "SWAN Server starting...")
		self.resources = resources #resource dictionary pool
		self.handlers = []
		self.add_handler(8)
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
		wfile = sock.makefile('wb',0)
		self.handle_request(sock, rfile, wfile)
	
	def handle_request(self, sock, rfile, wfile):
		#log.debug(self, "Handling connection from %s:%d" % sock.getpeername())
		sock.settimeout(2.0)
		raw_requestline = rfile.readline()
		sock.settimeout(None) #disable timeouts
		if not raw_requestline:
			log.debug(self, "No Request. Closing connection to %s:%d" % sock.getpeername())
			wfile.flush()
			sock.close()
			log.debug(self, "\n****************\n\n****************")
			return
		
		#got command, path, and request_version and headers
		command, path, http = raw_requestline.strip().split(' ')
		
		headers = {}
		headerline = rfile.readline()
		while not headerline.strip() == "":
			key, value = headerline.split(":",1)
			headers[key.strip()] = value.strip()
			headerline = rfile.readline()

		(responder_pool, specifier, params) = one(self.registries).lookup(path)
		#log.debug(self,"Responders: %s,\n Specifier: %s,\n Params: %s\n" % (responder_pool, specifier, params))
		request = Request(self, sock, rfile, wfile, command, path,  headers, params)
		handler = one(responder_pool)
		log.debug(self, "%s to %s" % (str(request), handler))
		handler.respond(request, specifier)
