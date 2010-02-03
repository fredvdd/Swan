from Actors.keywords import *
from Swan.filehandler import FileHandler
import socket
from BaseHTTPServer import BaseHTTPRequestHandler



class Server(LocalActor):
	
	def birth(self, address, port):
		print "SWAN Server starting..."
		self.handlers = [InitialHandler(n) for n in range(0,1)]
		
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

class InitialHandler(SocketActor, BaseHTTPRequestHandler):

	def birth(self, num):
		self.num = num
		self.default_request_version = "HTTP/1.1"
		self.fh = SlowEchoHandler()#FileHandler("/Users/fred/Documents/Year1/CogRob")
		
	def handle(self, sock, client_address):
		self.socket = sock.get_content()
		self.client_address = client_address
		print "Handling %s, %d" % self.client_address
		
		self.rfile = self.socket.makefile('rb',-1)
		self.wfile = self.socket.makefile('wb',0)
		
		self.close_connection = 0
		self.handle_request()
		while not self.close_connection:
			self.handle_request()
		
		self.finish()
		self.socket.close()
		print "request handled\n***********************************"
	
	def handle_request(self):
		self.fh.echo(self.rfile.readline(), self)
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


class SlowEchoHandler(MobileActor):

	def birth(self):
		pass

	def echo(self, request, writer):
		print "echoing request: %s" % request
		writer.write(request)
		print "echo sent"
		return	

class wrapper:
	def __init__(self, content):
		self.content = content

	def __deepcopy__(self, memo):
		return wrapper(self.content)

	def get_content(self):
		return self.content
