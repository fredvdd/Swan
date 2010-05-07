from Actors.keywords import *
from Actors.Device.file import File
from Actors.Device.db import SqliteDatabase
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import FileHandler, DefaultHandler, DatabaseHandler
from Swan.fields import *

class Users(DatabaseHandler):
	id = IntegerField()
	name = TextField()
	email = EmailField()

class Statuses(DatabaseHandler):
	status_id = IntegerField()
	user_id = IntegerField()
	status = TextField()
	timestamp = TimeField()

class Follows(DatabaseHandler):
	f_id = IntegerField()
	user_id = IntegerField()
	followed_user = IntegerField()
	
class Launcher(LocalActor):
	
	def birth(self, path):
		#find resources in path.
		#make a pool of each one.
		file_workers = pool([r.actor_id for r in [File() for n in range(0,5)]])
		db_workers = pool([r.actor_id for r in [SqliteDatabase('/Users/fred/swan/Swan/Test/database') for n in range(0,5)]])
		
		file_handlers = get_pool(FileHandler, "/Users/fred/swan/Swan/Test/html/", file_workers)
		user_handlers = get_pool(Users, db_workers)
		status_handlers = get_pool(Statuses, db_workers)
		follow_handlers = get_pool(Follows, db_workers)
	
		#create registry pool
		defaults = get_pool(DefaultHandler)
		registries = get_pool(Registry, defaults)
		
		all(registries).register('^/files/(?P<path>.*)$', file_handlers)
		all(registries).register('^/db/users/(?P<col>.*)/(?P<val>.*)$', user_handlers, 'detail')
		all(registries).register('^/db/users$', user_handlers)
		
		#launch server with registry pool
		Server("localhost", 8080, registries)

def start():
	Launcher("")
	#RootActor()

if __name__ == '__main__':
	initialise(start)
