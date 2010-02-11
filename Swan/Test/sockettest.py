from Actors.keywords import *
import socket
import os
import Actors.threadlocal
import random
from BaseHTTPServer import BaseHTTPRequestHandler

class TestActor(LocalActor):
	
	def birth(self, address, port):
		print "Test Actor!"
		#Init socket
		self.socket = open_socket(8080)
		while 1:
			self.accept()
		
	def accept(self):
		socket = self.socket.accept()
		socket.settimeout(2.0)
		asdf = socket.recv(16)
		print "Got %s" % asdf
	
# class RequestHandler(SocketActor, ResponseMixin):
# 	
# 	def birth(self, sock, client):
# 		self.socket, self.address = (sock, client)
# 		print self.socket
# 		print self.address
# 		#self.handle()
# 		#self.respond(self.socket.makefile('wb', 0), "boogaloo")
# 		#self.socket.close()
# 		#wfile = self.socket.makefile('wb', 0)
# 		#wfile.write("asdf")
# 		#for x in self.socket.makefile('rb', -1).readlines():
# 		#	print x #.write("HTTP/1.1 200 OK\n\r\r<h1>Hello</h1>\n\n")
# 	def handle(self, sock):
# 		self.socket = sock.get_socket()
# 		print "Joy"
# 		self.respond(self.socket.makefile('wb', 0), "boogaloo")

def start():
	print "Starting"
	TestActor("localhost", 8080)

if __name__ == '__main__':
    initialise(start)