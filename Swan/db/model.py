from Swan.db.query import *
from Swan.db.fields import IntegerField
import Swan.db.static
from Actors.keywords import *
import types

class Model(StaticActor):
	id = IntegerField()
	pool = None
	instance_type = None
	
	def birth(self, workers):
		self.workers = workers
		clazz = self.__class__
		self.table = clazz.__name__
		self.model_instance = clazz.instance_type
	
	def get_workers(self):
		return self.workers
	
	def set_pool(self, pool):
		self.__class__.pool = pool
		return pool
		
	def execute_select(self, query):
		cursor = self.workers.one().get_cursor().execute(query)
		rows = cursor.fetchall()
		cols = cursor.description()
		props = [dict(zip([col[0] for col in cols],row))for row in rows]
		return [self.model_instance(self, self.table, **ps) for ps in props]
	
	def execute_insert(self, query):
		cursor = self.workers.one().get_cursor()
		cursor.execute(query)
		return cursor.lastrowid()
	
	@classmethod
	def all(cls):
		return Query(cls.pool.one(), cls.__name__, **{})
	
	@classmethod
	def filter(cls, **kwds):
		return Query(cls.pool.one(), cls.__name__, **kwds)
	
	@classmethod
	def get(cls, **kwds):
		return SingleQuery(cls.pool.one(), cls.__name__, cls.instance_type, **kwds)
		
	@classmethod
	def create(cls, **kwds):
		return cls.instance_type(cls.pool.one(), cls.__name__, **kwds)
		
class ModelInstance(object):
	
	def __init__(self, model, table, **props):
		self.__model = model
		self.__table = table
		self.__dict__.update(props)
		
	def save(self):
		if hasattr(self,"id"):
			self._update()
		else:
			self._insert()
		return self
	
	def _insert(self):	
		cols = list()
		vals = list()
		for f in self.__class__.__dict__['__fields']:
			if self.__dict__.has_key(f):
				cols.append(f)
				vals.append(self.__dict__[f])
		m = lambda x: "'%s'" % x;
		r = lambda a, v: "%s, %s" % (a,v);
		cols_vals = (reduce(r, map(m, cols)), reduce(r, map(m, vals)))
		query = "INSERT INTO " + self.__table + ("(%s) VALUES (%s);" % cols_vals)
		self.id = self.__model.execute_insert(query)
	
	def _update(self):
		query = "UPDATE %s SET " % self.__table
		for f in self.__class__.__dict__['__fields']:
			if self.__dict__.has_key(f) and not f == 'id':
				query += "%s='%s'," % (f, self.__dict__[f])
		query = query[:-1] + " WHERE id = '%s'" % self.id
		print query
		print self.__model.execute_insert(query)