from Actors.keywords import *
from Swan.server import Server
from Swan.registry import Registry

def handle_directory():
	pass
	
class Launcher(LocalActor):
	
	def birth(self, path):
		#find resources in path.
		#make a pool of each one.
		echoes = get_pool(EchoHandler)
	
		#create registry pool
		registries = get_pool(Registry)
	
		registries.register([('/', echoes) for n in registries.actor_ids])
		
		#launch server with registry pool
		Server("localhost", 8080, registries)

class EchoHandler(StaticActor):

	def birth(self):
		print "Creating echo handler"
	
	def respond(self, method, specifier, params, headers, request):
		request.writer.write("%s %s %s %s" % (method, specifier, params, headers))

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

def start():
	Launcher("")
	#RootActor()

if __name__ == '__main__':
	initialise(start)