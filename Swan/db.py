import sys,types,sqlite3 as sql
from inspect import isclass
from Swan.fields import Field, IntegerField
from Actors.keywords import *

class Model(StaticActor):
	id = IntegerField()
	fields = {}
	set_names = {}
	
	def birth(self, workers):
		self.workers = workers
		clazz = self.__class__
		self.table = clazz.__name__
		self.fields = clazz.fields
		self.sets = clazz.set_names
		custom_funcs = dict([(x,y) for (x,y) in clazz.__dict__.iteritems() if isinstance(y, types.FunctionType)])
		self.model_instance = type(self.table +"Instance", (ModelInstance,), custom_funcs)
	
	def set_pool(self, pool):
		self.__class__.pool = pool
		
	def execute_query(self, query):
		print "executing query " + query 
		cols, rows = one(self.workers).execute(query)
		return [self.model_instance(zip([col[0] for col in cols],row)) for row in rows]
	
	@classmethod
	def all(cls):
		return Query(cls.pool.one(), cls.__name__, **{})
	
	@classmethod
	def filter(cls, **kwds):
		return Query(cls.pool.one(), cls.__name__, **kwds)
		
class ModelInstance(object):
	
	def __init__(self, props):
		self.__dict__.update(props)

class Query(object):
	
	def __init__(self, model, table, **filters):
		self.model = model
		self.table = table
		self.filters = filters
		self.cache = []
		self.cached= False

	def filter(self, **filters):
		temp_filters = self.filters
		temp_filters.update(filters)
		return Query(self.model, self.table, **temp_filters)
		
	def build_filter_string(self):
		if len(self.filters) < 1:
			return ""
		return "WHERE " + reduce(lambda s, (p,v): "%s %s AND %s" % (p,v,s), self.filters.iteritems(), "")[:-4]
		
	def populate_cache(self):
		filter_string = self.build_filter_string()
		query = "SELECT * FROM %s %s" % (self.table, filter_string)
		results = self.model.execute_query(query)
		self.cache = results
		self.cached = True
		
	def __iter__(self):
		if not self.cached:
			self.populate_cache()
		return iter(self.cache)

	def __repr__(self):
		if not self.cached:
			self.populate_cache()
		return str(self.cache)
			

def equals(value):
	return "= '%s'" % value
	
def less_than(value):
	return "< %s" % value

def greater_than(value):
	return "> %s" % value

			
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
		create = 'CREATE TABLE %s (\n\t"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,\n' % name
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
		c.execute(query)
	conn.commit()
	c.close()

if __name__ == '__main__':
	sitepath = sys.argv[1]
	sync(sitepath)