from Actors.keywords import *
from Swan.request import Request
from Swan.static import log
from BaseHTTPServer import BaseHTTPRequestHandler
from itertools import cycle
from threading import Timer

class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port, resources):
		log.debug(self, "SWAN Server starting...")
		self.resources = resources #resource dictionary pool
		self.handlers = []
		self.add_handler(1)
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

class RequestHandler(LocalActor, BaseHTTPRequestHandler):
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
		self.rfile = rfile
		self.wfile = wfile
		sock.settimeout(2.0)
		self.raw_requestline = self.rfile.readline()
		log.debug(self, "Request headline:%s" % self.raw_requestline)
		sock.settimeout(None) #disable timeouts
		if not self.raw_requestline or not self.parse_request():
			log.debug(self, "Closing connection to %s:%d" % sock.getpeername())
			wfile.flush()
			sock.close()
			return
		#got command, path, and request_version and headers
		#log.debug(self,"Command: %s,\n Path: %s,\n Headers: %s\n" % (self.command, self.path, self.headers))
		command, path, headers = (self.command, self.path, self.headers)
		(responder_pool, specifier, params) = one(self.registries).lookup(path)
		#log.debug(self,"Responders: %s,\n Specifier: %s,\n Params: %s\n" % (responder_pool, specifier, params))
		request = Request(self, sock, rfile, wfile, command, path,  headers, params)
		handler = one(responder_pool)
		log.debug(self, "%s to %s" % (str(request), handler))
		handler.respond(request, specifier)

	def log_message(self, format, *args):
		pass