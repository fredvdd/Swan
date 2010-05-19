from Actors.keywords import *
from Actors.Device.file import File
from Actors.Device.db import SqliteDatabase
from Swan.server import Server
from Swan.registry import Registry
from Swan.handlers import FileHandler, DefaultHandler, DatabaseHandler
from Swan.fields import Field, ForeignKey
from Swan.db import Model, extract_models
from Swan.Test.honker.models import Users, Statuses
import sys

def init_db_models(modelpath):
	print "Extracting models from " + modelpath
	models = extract_models(modelpath)
	print models
	fkss = dict([[x,{}] for x in models])
	for model in models:
		print "Initialising " + model
		fields = {}
		for p in models[model].__mro__:
			if issubclass(p, Model):
				print "Inspecting " + str(p) + " for fields"
				props = p.__dict__
				for prop in props:
					if isinstance(props[prop], Field):
						fields[prop] = props[prop].__class__
					if isinstance(props[prop], ForeignKey):
						fk = props[prop]
						print fk.table + " -> " + model + "/" + fk.name
						fkss[fk.table].update({fk.name:model})
		models[model].fields = fields
	for fks in fkss:
		models[fks].set_names = fkss[fks]
	return models
	
	
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
			model_pool.all().set_pool(model_pool)
			model_pools[x] = model_pool
			
		print model_pools
		
		Statuses.filter(id=4)
		Users.filter(name="Fred")
		
		# file_handlers = get_pool(FileHandler, "/Users/fred/swan/Swan/Test/html/", file_workers)
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
