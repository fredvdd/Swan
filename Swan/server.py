from Actors.keywords import *
from Swan.filehandler import FileHandler
import socket
from BaseHTTPServer import BaseHTTPRequestHandler
from itertools import cycle

class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port, resources):
		print "SWAN Server starting..."
		self.resources = resources #resource dictionary pool
		self.handlers = []
		self.add_handler(5)
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
		self.handler_cycle.next().handle(self.sock.accept())
		
	def add_handler(self, count = 1):
		self.handlers.extend([RequestHandler(self.resources) for n in range(0,count)])
		self.handler_cycle = cycle(self.handlers)

class TestResponseMixin(object):

	def respond(self, outfile, request):
		outfile.write("%s %d %s\r\n" % ("HTTP/1.1", 200, "OK"))
		outfile.write("%s: %s\r\n" % ("Content-type", "text/html"))
		outfile.write("\r\n")
		outfile.write("<html><head><title>Title goes here.</title></head>")
		outfile.write("<body><p>This is a test.</p>")
		outfile.write("<p>Request was to: %s</p>" % request)
		outfile.write("</body></html>")
		outfile.flush()
		#outfile.close()

class RequestHandler(LocalActor, BaseHTTPRequestHandler, TestResponseMixin):
	"""Reads request method, resource and headers"""

	def birth(self, registries):
		self.default_request_version = "HTTP/1.1" #needed for parse_request
		self.registries = registries
		
	def handle(self, sock):
		self.socket = sock
		self.client_address = sock.getsockname()
		print "Handling %s, %d" % self.client_address
		self.rfile = self.socket.makefile('rb',-1)
		self.wfile = self.socket.makefile('wb',0)
		
		self.close_connection = 0
		self.handle_request()
		while not self.close_connection:
			self.handle_request()
		#self.finish()
		#self.socket.close()
	
	def handle_request(self):
		self.raw_requestline = self.rfile.readline()
		if not self.raw_requestline:
			self.close_connection = 1
			return
		if not self.parse_request():
			return
		#got command, path, and request_version and headers
		request = dict(client=self.socket,reader=self.rfile,writer=self.wfile)
		(responder_pool, specifier, params) = one(self.registries).lookup(self.path)
		one(responder_pool).respond(self.command, specifier, params, self.headers, request)

	def log_message(self, format, *args):
		pass
		
class Request(object):
	
	def __init__(self, socket, rfile, wfile):
		self.socket = socket
		self.wfile = wfile
		self.rfile = rfile
		
	def finish(self):
		self.wfile.flush()
		self.socket.close()
		
	def respond(self, string):
		self.wfile.write(string)
		