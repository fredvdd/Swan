from Actors.keywords import *
from Actors.Device.file import File
from Actors.Device.db import SqliteDatabase
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import FileHandler, DefaultHandler, DatabaseHandler
from Swan.Test.tester import Test
from Swan.db import init_db_models
import sys


	
	
class Launcher(LocalActor):
	
	def birth(self, path, models):
		print path
		#find resources in path.
		#make a pool of each one.
		file_workers = pool([r.actor_id for r in [File() for n in range(0,5)]])
		db_workers = pool([r.actor_id for r in [SqliteDatabase(path+"database") for n in range(0,5)]])
		
		model_pools = {}
		for (x,y) in models.iteritems():
			model_pool = get_pool(y, db_workers)
			setting = model_pool.all().set_pool(model_pool)
			model_pools[x] = model_pool
			
		print "****"
		
		t = Test()
		print t.start()
		
		# for user in Users.get(name=equals('Fred')):
		# 	print user
		# 
		# p = Users.get(name=equals('Pete'))
		# print p
		
		# for user in Users.get(name=equals('Fred')):
		# 	print user
		# print Users.filter(name="Fred")
		# for x in Statuses.filter(id=5):
		# 	print x,
			
		print "DOne"
		
		# file_handlers = get_pool(FileHandler, "/Users/fred/swan/Swan/Test/html/", file_workers)
		# print file_handlers
		# user_handlers = get_pool(Users, db_workers)
		# status_handlers = get_pool(Statuses, db_workers)
		# follow_handlers = get_pool(Follows, db_workers)
		# 	
		# #create registry pool
		# defaults = get_pool(DefaultHandler)
		# registries = get_pool(Registry, defaults)
		# 
		# all(registries).register('^/files/(?P<path>.*)$', file_handlers)
		# all(registries).register('^/db/users/(?P<col>.*)/(?P<val>.*)$', user_handlers, 'detail')
		# all(registries).register('^/db/users$', user_handlers)
		# all(registries).register('^/db/statuses/(?P<col>.*)/(?P<val>.*)$', status_handlers, 'detail')
		# # all(registries).register(
		# 
		# #launch server with registry pool
		# Server("localhost", 8080, registries)

def start(path, models):
	Launcher(path, models)
	#RootActor()

if __name__ == '__main__':
	path = sys.argv[1]
	path = path if path.endswith("/") else path+"/"
	dbpath = path + 'database'
	modelpath = path.replace('/','.') + 'models'
	models = init_db_models(modelpath)
	initialise(start, *[path, models])
