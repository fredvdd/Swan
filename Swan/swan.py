from Actors.keywords import *
from Actors.Device.file import File
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import FileHandler, DefaultHandler

def handle_directory():
	pass
	
class Launcher(LocalActor):
	
	def birth(self, path):
		#find resources in path.
		#make a pool of each one.
		file_workers = pool([r.actor_id for r in [File() for n in range(0,5)]])
		
		file_handlers = get_pool(FileHandler, "/Users/fred/swan/Swan/Test/html/", file_workers)
	
		#create registry pool
		defaults = get_pool(DefaultHandler)
		registries = get_pool(Registry, defaults)
		
		all(registries).register('/files/(?P<path>.*)', file_handlers)
		
		#launch server with registry pool
		Server("localhost", 8080, registries)

def start():
	Launcher("")
	#RootActor()

if __name__ == '__main__':
	initialise(start)
