from Actors.keywords import *
from Actors.Device import file, db
from Swan.server import *
from Swan.db import init_db_models
from Swan.swanjs import *
import sys, os.path
from inspect import isclass

class Launcher(LocalActor):
	
	def birth(self, path, models):
		filepath = os.path.abspath(path)
		print filepath
		print "Launching server for %s..." % path
		
		#create low-level workers
		print "Creating Worker pools..."
		file_workers = pool([r.actor_id for r in [file.File() for n in range(0,5)]])
		db_workers = pool([r.actor_id for r in [db.SqliteDatabase(path+"database") for n in range(0,5)]])
		
		#create model pools
		model_pools = dict()
		print "Creating Model pools...\n",
		for (n,m) in models.iteritems():
			print "\t",
			model_pool = get_pool(m, db_workers)
			setting = model_pool.all().set_pool(model_pool)
			model_pools[n] = model_pool
		
		#create error handlers
		print "Creating default handlers...\n\t",
		defaults = get_pool(DefaultHandler)
		#create handler registry
		print "Creating registry...\n\t",
		registries = get_pool(Registry, defaults)
		
		#create custom handlers
		handlerpath = path.replace('/','.') + 'handlers'
		print "Loading handlers from %s...\n" % handlerpath,
		handlermod = __import__(handlerpath, globals(), locals(), [''])
		handler_pools = dict()
		for ek in dir(handlermod):
			ev = getattr(handlermod, ek)
			if isclass(ev) and issubclass(ev, Handler):
				if ev.__name__ == 'Handler' or ev.__name__ == 'FileHandler':
					continue
				if issubclass(ev, FileHandler):
					print "\t",
					handler_pools[ek] = get_pool(ev, filepath + getattr(ev,'root'),file_workers)
					all(registries).register(getattr(ev,'bindings')['default'],handler_pools[ek])
				else:
					bindings = getattr(ev, 'bindings')
					print "\t",
					handler_pools[ek] = get_pool(ev)
					for (s,p) in bindings.iteritems():
						all(registries).register(p,handler_pools[ek],(s if not s == 'default' else None))
		# Test().start()
		
		print "Starting server..."
		# #launch server with registry pool
		Server("localhost", 8080, registries)

def start(path, models):
	Launcher(path, models)

options = {'kitchensink':3,'launch':2,'compile':1}

if __name__ == '__main__':
	runlevel = options[sys.argv[1]]
	path = sys.argv[2]
	if runlevel & 1 == 1:#compile
		print "Compiling..."
		filepath = os.path.abspath(path)
		output_js(add_handlers(translate_source([filepath+"/view.py"]), filepath+"/handlers"), filepath+"/files/index")
		
		
	if runlevel & 2 == 2:#launch
		print "Initialising server..."
		path = path if path.endswith("/") else path+"/"
		dbpath = path + 'database'
		modelpath = path.replace('/','.') + 'models'
		models = init_db_models(modelpath)
		initialise(start, *[path, models])
