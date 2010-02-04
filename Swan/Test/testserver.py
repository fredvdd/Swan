import time
import BaseHTTPServer
from Actors.keywords import *
from Swan.server import Server
from Host.static import local_theatre
from time import sleep

class RootActor(LocalActor):
	
	def birth(self):
		ServerActor(8080)
		#ClientActor(8080)

class ServerActor(LocalActor):
		
	def birth(self, port):
		print local_theatre().gethostname()
		local_theatre().say_hello()
		opened = open_socket(port)
		print opened
		print opened.getsockname()
		#ClientActor(opened)
		new_socket = opened.accept()
		print new_socket
		rfile = new_socket.makefile('r')
		wfile = new_socket.makefile('w')
		print wfile
		while 1:
			print "Reading data..."
			data = rfile.readline()
		 	if not data or len(data.strip()) < 1: break
			wfile.write("Echo: %s" % data)
			wfile.flush()
		new_socket.close()
		opened.close()
		print "Done"
		
		
class ClientActor(LocalActor):
	
	def birth(self, port):
		print local_theatre().gethostname()
		sleep(1)
		port.getsockname()
		# local_theatre().say_hello()
		# sleep(1)
		# print "Connecting"
		# sock = connect_socket(('localhost', port))
		# print sock
		#opened = open_socket(port)
		#print opened
		#print opened.getsockname()
		#print opened.accept()
		#if opened:
		#	conn_id = local_theatre().accept_port(port)
		#	print "%s -> %s" % (opened, conn_id)
		#	local_theatre().close_port(port)
		#	print local_theatre().read_port(conn_id, 4)
		

def start():
    Server("localhost", 8080)
	#RootActor()

if __name__ == '__main__':
    initialise(start)
