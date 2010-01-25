from Actors.keywords import *
from Swan.filehandler import FileHandler
import socket
from BaseHTTPServer import BaseHTTPRequestHandler



class Server(LocalActor):
	
	def birth(self, address, port):
		print "SWAN Server starting..."
		self.handlers = [RequestHandler(n) for n in range(0,5)]
		
		#Init socket
		self.request_version = 'HTTP/1.1'
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((address, port))
		self.socket.listen(5)
		self.accept()
		
	def accept(self):
	 	current = 0
		while 1:
			try:
				rsock, client_address = self.socket.accept()
				self.handlers[current].handle(wrapper(rsock), client_address)
				print "sent!"
				current = (current + 1) % len(self.handlers)
			except KeyboardInterrupt:
				self.socket.flush()
				self.socket.close()

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

class RequestHandler(SocketActor, BaseHTTPRequestHandler, TestResponseMixin):

	def birth(self, num):
		self.num = num
		self.default_request_version = "HTTP/1.1"
		
	def handle(self, sock, client_address):
		self.socket = sock.get_content()
		self.client_address = client_address
		print "Handling %s, %d" % self.client_address
		self.rfile = self.socket.makefile('rb',-1)
		self.wfile = self.socket.makefile('wb',0)
		
		self.close_connection = 1
		self.handle_request()
		while not self.close_connection:
			self.handle_request()
		
		self.finish()
		self.socket.close()
		print "request handled\n***********************************"
	
	def handle_request(self):
		self.raw_requestline = self.rfile.readline()
		if not self.raw_requestline:
			self.close_connection = 1
			return
		if not self.parse_request():
			return
		print "%s, %s, %s" % (self.command, self.path, self.request_version)
		for header in self.headers:
			print header + " : " + self.headers.get(header, "")
		#self.respond(self.wfile, self.path + " handled by " + str(self.num))
		fh = FileHandler("/homes/jv06/public_html/")
		self.wfile.write(fh.get(self.path))
		self.wfile.flush()

class wrapper:
	def __init__(self, content):
		self.content = content

	def __deepcopy__(self, memo):
		return self

	def get_content(self):
		return self.content
