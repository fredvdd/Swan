import time
import BaseHTTPServer
from Actors.keywords import *
from Swan.server import Server
from Host.static import local_theatre
#from time import sleep

class RootActor(LocalActor):
	
	def birth(self):
		TestActor(8080)
		TestActor(8090)

class TestActor(LocalActor):
	
	def birth(self, port):
		print local_theatre().gethostname()
		local_theatre().say_hello()
		opened = local_theatre().open_port(port)
		if opened:
			conn_id = local_theatre().accept_port(port)
			print "%s -> %s" % (opened, conn_id)
			local_theatre().close_port(port)
			print local_theatre().read_port(conn_id, 4)
		

def start():
    #Server("localhost", 8080)
	RootActor()

if __name__ == '__main__':
    initialise(start)