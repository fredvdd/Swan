from Actors.keywords import *
from Swan.request import Request
from BaseHTTPServer import BaseHTTPRequestHandler
from itertools import cycle
import socket

class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port, resources):
		print "SWAN Server starting..."
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
		print "Waiting for connection"
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
		print "Handling %s, %d" % sock.getpeername()
		rfile = sock.makefile('rb',-1)
		wfile = sock.makefile('wb',0)
		
		self.handle_request(sock, rfile, wfile)
	
	def handle_request(self, sock, rfile, wfile):
		self.rfile = rfile
		#self.raw_requestline = self.rfile.readline()
		sock.settimeout(5.0)
		buffers = []
		data = None
		while data != "\n":
			data = sock.recv(1)
			if not data:
				break
			buffers.append(data)
		sock.settimeout(None)
		self.raw_requestline = "".join(buffers)
		if not self.raw_requestline:
			self.close_connection(sock, wfile)
		if not self.parse_request():
			self.close_connection(sock, wfile)
		#got command, path, and request_version and headers
		command, path, headers = (self.command, self.path, self.headers)
		(responder_pool, specifier, params) = one(self.registries).lookup(path)
		request = Request(self, sock, rfile, wfile, path,  headers, params)
		one(responder_pool).respond(command, specifier, request)
	
	def close_connection(self, sock, wfile):
		print "Closing connection"
		wfile.flush()
		sock.close()

	def log_message(self, format, *args):
		pass