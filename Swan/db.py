import sys,sqlite3 as sql
from inspect import isclass
from Swan.fields import Field, IntegerField
from Actors.keywords import StaticActor

class Model(StaticActor):
	id = IntegerField()
	fields = {}
	set_names = {}
	
	def birth(self, workers):
		self.workers = workers
		self.fields = self.__class__.fields
		self.sets = self.__class__.set_names
	
	def set_pool(self, pool):
		self.__class__.pool = pool
	
	@classmethod
	def all(cls):
		print cls.pool
		#return Query(cls.pool.one(), **{})
	
	@classmethod
	def filter(cls, **kwds):
		print kwds
		#return Query(cls.pool.one(), **kwds)
	
	
	

def extract_models(modelpath):
	module = __import__(modelpath, globals(), locals(), [''])
	models = {}
	for x in dir(module):
		 if isclass(module.__dict__[x]) and module.__dict__[x].__bases__[0].__name__ == "Model":
			models[x] = module.__dict__[x]													
	return models

def get_sql(table_definitions):
	creates = []
	for name in table_definitions:
		fields = table_definitions[name].__dict__
		create = 'CREATE TABLE %s (\n\t"id" serial NOT NULL PRIMARY KEY,\n' % name
		for x in fields:
			if isinstance(fields[x], Field):
				create += '\t"%s" %s,\n' % (x,fields[x].field_type())
		create = create[:-2] + "\n);\n"
		creates.append(create)
	return creates

def sync(sitepath):
	modelpath = sitepath.replace('/','.') + ("models" if sitepath.endswith("/") else ".models") 
	queries = get_sql(extract_models(modelpath))
	databasepath = sitepath + ("database" if sitepath.endswith("/") else "/database")
	conn = sql.connect(databasepath)
	c = conn.cursor()
	for query in queries:
		print query
		#c.execute(query)
	conn.commit()
	c.close()

if __name__ == '__main__':
	sitepath = sys.argv[1]
	sync(sitepath)