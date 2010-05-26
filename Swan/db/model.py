from Actors.keywords import *
from Swan.db.fields import IntegerField, ForeignKey
from Swan.db.query import Query, SingleQuery, ForeignRelation
import types
from Swan.static import log

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
		log.debug(self, "Executing SQL: " + query)
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
		# log.debug(None, "Creating %s" % self.__class__.__name__)
		self.__model = model
		self.__table = table
		#self.__dict__.update(props)
		# print "Class fields %s" % (self.__class__.__dict__['__fields'])
		fields = self.__class__.__dict__['__fields']
		for p in props:
			self.__dict__[p] = props[p]
			if fields.has_key(p) and isinstance(fields[p], ForeignRelation) and not isinstance(props[p], SingleQuery):
				rel = fields[p]
				fil = dict({'id':"='%s'"%props[p]})
				log.debug(None,"Creating query for %s" % p)
				asdf = SingleQuery(rel.join_table.pool.one(), rel.join_name, rel.join_table.instance_type, **fil)
				self.__dict__[p] = asdf
				
	def __getattribute__(self, name):
		# log.debug(None, "asked for attribute %s" % name)
		attr = object.__getattribute__(self, name)
		if isinstance(attr, ForeignRelation):
			log.debug(None, "asked for attribute %s" % name)
			fil = {'id' : equals(object.__getattribute__(self,'id'))}
			return RelationSet(attr,self.__model,self.__table,**fil)
		return attr
	
	def __deepcopy__(self, memo):
		# log.debug(None, "Deepcopying %s" % self.__class__.__name__)
		return self.__class__(self.__model, self.__table, **dict([(f,self.__dict__[f]) for f in self.__class__.__dict__['__fields']]))
	
	def __getstate__(self):
		return (self.__model, self.__table) + tuple([(f,self.__dict__[f]) for f in self.__class__.__dict__['__fields']])
		
	def __setstate__(self,state):
		self.__model, self.__table = state[:2]
		self.__dict__.update(dict(state[2:]))
		
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