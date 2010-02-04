from Actors.keywords import *
from Swan.filehandler import FileHandler
import socket
from BaseHTTPServer import BaseHTTPRequestHandler



class Server(LocalActor):
	"""Root actor with accepting socket, simply accepts 
connections and passes them on"""
	def birth(self, address, port):
		print "SWAN Server starting..."
		self.handlers = [RequestHandler(n) for n in range(0,1)]
		self.sock = open_socket(port)
		self.accept()
		
	def accept(self):
	 	current = 0
		while 1:
			try:
				client_sock = self.sock.accept()
				self.handlers[current].handle(client_sock)
				current = (current + 1) % len(self.handlers)
			except KeyboardInterrupt:
				self.sock.close()

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

class RequestHandler(LocalActor, BaseHTTPRequestHandler):
	"""Reads request method, resource and headers"""

	def birth(self, num):
		self.num = num
		self.default_request_version = "HTTP/1.1"
		self.fh = EchoHandler()#FileHandler("/Users/fred/Documents/Year1/CogRob")
		
	def handle(self, sock):
		self.socket = sock
		self.client_address = sock.getsockname()
		print "Handling %s, %d" % self.client_address
		self.rfile = self.socket.makefile('rb',-1)
		self.wfile = self.socket.makefile('wb',0)
		
		#self.close_connection = 0
		self.handle_request()
		#while not self.close_connection:
		#	self.handle_request()
		
		#self.finish()
		#self.socket.close()
		#print "request handled\n***********************************"
	
	def handle_request(self):
		self.fh.echo(self.rfile, self.wfile)
#		callback('write', self.fh.echo(self.rfile.readline()))
#		self.raw_requestline = self.rfile.readline()
#		if not self.raw_requestline:
#			self.close_connection = 1
#			return
#		if not self.parse_request():
#			return
#		print "%s, %s, %s" % (self.command, self.path, self.request_version)
#		response = self.path + "<dl>"
#		for header in self.headers:
#			print header + " : " + self.headers.get(header, "")
#			response += "<dt><b>%s</b></dt><dd>%s</dd>" % (header, self.headers.get(header, ""))
#		self.wfile.write(self.fh.get(self.path))
#		self.wfile.flush()

	def write(self, the_str):
		print "hello"
		self.wfile.write(the_str)
	
	def log_message(self, format, *args):
		pass


class EchoHandler(MobileActor):

	def birth(self):
		pass

	def echo(self, rfile, wfile):
		while True:
			request = rfile.readline()
			print "Echo: %s" % request
			if not request or len(request.strip()) < 1:
				break
			wfile.write(request)
			wfile.flush()
		wfile.close()
		print "echo sent"
		return	
