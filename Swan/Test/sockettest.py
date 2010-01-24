from Actors.keywords import *
import socket
import os
import Actors.threadlocal
import random
from BaseHTTPServer import BaseHTTPRequestHandler

class ResponseMixin(object):
	
	def respond(self, outfile, request):
		outfile.write("%s %d %s\r\n" % ("HTTP/1.1", 200, "OK"))
		outfile.write("%s: %s\r\n" % ("Content-type", "text/html"))
		outfile.write("\r\n")
		outfile.write("<html><head><title>Title goes here.</title></head>")
		outfile.write("<body><p>This is a test.</p>")
		outfile.write("<p>Request was: %s</p>" % request)
		outfile.write("</body></html>")
		outfile.flush()
		outfile.close()

class TestActor(LocalActor):
	
	def birth(self, address, port):
		print "Test Actor!"
		#Init socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((address, port))
		self.socket.listen(5)
		self.accept()
		self.request_version = 'HTTP/1.1'
		
	def accept(self):
		while 1:
			try:
				rsock, client_address = self.socket.accept()
				#RequestHandler(SwanSocket(rsock), client_address)
				asdf = RequestHandler("one", "two")
				asdf.handle(SwanSocket(rsock))
				#rsock.makefile('wb',0).write("HTTP/1.1 200 OK\n\r\r<h1>Hello</h1>\n\n")
				#self.wfile = rsock.makefile('wb',0)
				#self.rfile = rsock.makefile('rb', -1)
				#request = self.rfile.readline()
				#self.respond(self.wfile, request)
				#print request
				print "sent!"
			except KeyboardInterrupt:
				self.socket.flush()
				self.socket.close()
			
		#ta = TestActorB(SwanSocket(clisock))
		#print clisock._sock
		#print clisock.fileno()
		#print clisock.makefile('w',0).fileno()
		#ta.__send__(clisock._sock)
		
class RequestHandler(SocketActor, ResponseMixin):
	
	def birth(self, sock, client):
		self.socket, self.address = (sock, client)
		print self.socket
		print self.address
		#self.handle()
		#self.respond(self.socket.makefile('wb', 0), "boogaloo")
		#self.socket.close()
		#wfile = self.socket.makefile('wb', 0)
		#wfile.write("asdf")
		#for x in self.socket.makefile('rb', -1).readlines():
		#	print x #.write("HTTP/1.1 200 OK\n\r\r<h1>Hello</h1>\n\n")
	def handle(self, sock):
		self.socket = sock.get_socket()
		print "Joy"
		self.respond(self.socket.makefile('wb', 0), "boogaloo")

class SwanSocket:
	def __init__(self, socket):
		self.sock = socket

	def __deepcopy__(self, memo):
		return self

	def get_socket(self):
		return self.sock

def start():
	print "Starting"
	TestActor("localhost", 8080)
	#asd = raw_input("sup? ")
	#asdf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#asdf.connect(('localhost', 8080))
	
	#psqh = SocketActorTest(asdf, "first", "second")
	#zxcv = TestActorB(psqh)

if __name__ == '__main__':
    initialise(start)