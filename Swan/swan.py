from Actors.keywords import *
from Actors.Device.file import File
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import EchoHandler, FileHandler

def handle_directory():
	pass
	
class Launcher(LocalActor):
	
	def birth(self, path):
		#find resources in path.
		#make a pool of each one.
		file_workers = pool([r.actor_id for r in [File() for n in range(0,5)]])
		
		echoes = get_pool(EchoHandler)
		file_handlers = get_pool(FileHandler, "/Users/fred/Dropbox/Documents/Year1/CogRob/", file_workers)
	
		#create registry pool
		registries = get_pool(Registry)
		
		all(registries).register('/files/(?P<path>.*)', file_handlers)
		all(registries).register('/', echoes)
		
		#launch server with registry pool
		Server("localhost", 8080, registries)

def start():
	Launcher("")
	#RootActor()

if __name__ == '__main__':
	initialise(start)
