from Actors.keywords import *
import socket

class Server(LocalActor):
	
	def birth(self, address, port):
		print "SWAN Server starting..."
		#Init handlers
		#self.handlers = [RequestHandler(n) for n in range(0,5)]
		
		self.sockets = {}
		
		#Init socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((address, port))
		self.server_address = self.socket.getsockname()
		self.host_ip, self.server_port = self.server_address[:2]
		self.server_name = socket.getfqdn(self.host_ip)
		print "Socket " + self.server_name + "(" + self.host_ip + ") on port " + str(self.server_port)
		self.socket.listen(5)
		self.accept()
		
	def accept(self):
		n = 0
		while 1:
			try:
				rsock, client_address = self.socket.accept()
				self.sockets[client_address] = rsock
				
				ssock = SwanSocket(rsock)
				ta = TestActor()
				ta.ping(ssock)
				
				rfile = rsock.makefile('rb', -1) 
				rstrings = [line.strip() for line in rfile.readlines()]
				print rstrings
				
				#self.handlers[n].handle(client_address, rstrings, self)
				
				n = (n + 1) % len(self.handlers)
			except KeyboardInterrupt:
				self.socket.close()
				self.close()
				
	def respond(self, response):
		print "oy"
		addr, resp = response
		req = self.sockets.pop(addr)
		wfile = req.makefile('wb',0)
		wfile.write(resp)
		wfile.flush()
		wfile.close()
		req.close()
		print "joy"
	
	def close(self):
		self.socket.close()
		self.die()
		
class SwanSocket:
	def __init__(self, socket):
		self.sock = socket
	
	def __deepcopy__(self, memo):
		return self
		
	def get_socket(self):
		return self.sock
		
class TestActor(MobileActor):
	def birth(self):
		print "Enter TestActor, stage left"
		
	def ping(self, msg):
		print "Pinged"
	
class RequestHandler(MobileActor):
	
	def birth(self, num):
		self.num = num
		print "Request Handler "+ str(num) + " born"
		
	def handle(self, client_address, request, responder):
		print str(self.num) + " says ASdf"
		print client_address
		responder.respond(client_address, "HTTP/1.1 404 Not Found")
		