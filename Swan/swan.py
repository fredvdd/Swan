from Actors.keywords import *
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import EchoHandler, FileHandler

def handle_directory():
	pass
	
class Launcher(LocalActor):
	
	def birth(self, path):
		#find resources in path.
		#make a pool of each one.
		echoes = get_pool(EchoHandler)
		files = get_pool(FileHandler, "/Users/fred/Dropbox/Documents/Year1/CogRob/")
	
		#create registry pool
		registries = get_pool(Registry)
		
		all(registries).register('/files/(?P<path>.*)', files)
		all(registries).register('/', echoes)
		
		#launch server with registry pool
		Server("localhost", 8080, registries)

def start():
	Launcher("")
	#RootActor()

if __name__ == '__main__':
	initialise(start)
