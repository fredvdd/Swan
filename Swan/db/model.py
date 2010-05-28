from Actors.keywords import *
from fields import IntegerField, ForeignKey
from query import Query, RelationSet
from relation import ForeignRelation
import types
from Swan.db import log

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
		
	def execute_select(self, desc, query):
		log.debug(self, "Executing SQL: " + query)
		cursor = self.workers.one().get_cursor().execute(query)
		rows = cursor.fetchall()
		props = [dict(zip(desc,row))for row in rows]
		return [self.model_instance(self, self.table, **ps) for ps in props]
	
	def execute_insert(self, query):
		cursor = self.workers.one().get_cursor()
		cursor.execute(query)
		return cursor.lastrowid()
	
	@classmethod
	def all(cls):
		return Query(cls.pool.one(), cls.__name__, cls.instance_type, **{})
	
	@classmethod
	def filter(cls, **kwds):
		return Query(cls.pool.one(), cls.__name__, cls.instance_type, **kwds)
	
	@classmethod
	def get(cls, **kwds):
		return PotentialModelInstance(cls.pool.one(), cls.__name__, cls.instance_type, **kwds)
		
	@classmethod
	def create(cls, **kwds):
		# print "Creating %s with %s" % (cls.instance_type.__name__, kwds)
		return cls.instance_type(cls.pool.one(), cls.__name__, **kwds)
		
class PotentialModelInstance(Query):

	def __init__(self, model, table, instance_type, **filters):
		# print "Single Query: %s, %s, %s, %s" % (model, table, instance_type, filters)
		Query.__init__(self, model, table, instance_type, **filters)

	def evaluate(self):
		return self._evaluate()[0]

	def __getattribute__(self, name):
		if name not in ['__repr__','__len__', '__iter__', '__getitem__']:
			try:
				return object.__getattribute__(self, name)
			except AttributeError:
				it = object.__getattribute__(self,'instance_type')
				if hasattr(it,name) or it.__dict__['__fields'].has_key(name):
					if it.__dict__.has_key(name) and isinstance(it.__dict__[name], ForeignRelation):
						return RelationSet(it.__dict__[name],object.__getattribute__(self, 'model'), object.__getattribute__(self,'table'), **object.__getattribute__(self, 'filters'))
				if not object.__getattribute__(self, 'cached'):
					log.debug(None, "Getting cache for %s access" % name)
					object.__getattribute__(self, '_check_cache')()
					# object.__setattr__(self, 'cache', object.__getattribute__(self, 'evaluate')())
					# object.__setattr__(self, 'cached', True)
					return object.__getattribute__(self.cache,name)
		# return object.__getattribute__(self,name)

	def __deepcopy__(self, memo):
		return SingleQuery(self.model.__deepcopy__(memo), self.table, self.instance_type, **self.filters)

	def __getstate__(self):
		return (self.model, self.table, self.filters, self.instance_type)

	def __setstate__(self, state):
		self.model, self.table, self.filters, self.instance_type = state
		self.cache = []
		self.cached = False
		
class ModelInstance(object):
	__fields = None
	
	def __init__(self, model, table, **props):
		# log.debug(None, "Creating %s with props %s" % (self.__class__.__name__, props))
		self.__model = model
		self.__table = table
		#self.__dict__.update(props)
		# print "Class fields %s" % (self.__class__.__dict__['__fields'])
		fields = getattr(self.__class__,'__fields')
		for f in fields:
			if isinstance(fields[f], ForeignRelation):
				relation = fields[f]
				rtable = relation.join_table
				if not props.has_key(f):
					rfields = getattr(rtable.instance_type, '__fields')
					rprops = dict([(rf,props['User.'+rf]) for rf in rfields])
					# print rprops
					self.__dict__[f] = rtable.instance_type(rtable, relation.join_name, **rprops)
				else:
					rf = props[f]
					if isinstance(rf, PotentialModelInstance) or isinstance(rf, ModelInstance):
						self.__dict__[f] = props[f]
					else:
						self.__dict__[f] = rtable.get(**{'id':"=%s"%props[f]})
			elif f == 'id':
				self.__dict__[f] = props[f] if props.has_key(f) else (props[table+'.id'] if props.has_key(table+'.id') else None)
			else:
				self.__dict__[f] = props[f] if props.has_key(f) else None;

	def __getattribute__(self, name):
		# log.debug(object.__getattribute__(self, '__class__'), "asked for attribute %s" % name)
		attr = object.__getattribute__(self, name)
		if isinstance(attr, PotentialModelInstance):
			log.debug(object.__getattribute__(self, '__class__').__name__, "asked for PotentialModelInstance attribute %s" % name)
		if isinstance(attr, ForeignRelation):
			log.debug(None, "asked for attribute %s" % name)
			fil = {'id' : equals(object.__getattribute__(self,'id'))}
			return RelationSet(attr,self.__model,self.__table,**fil)
		return attr
	
	def __deepcopy__(self, memo):
		# log.debug(None, "Deepcopying %s" % self.__class__.__name__)
		props = dict([(f,self.__dict__[f]) for f in self.__class__.__dict__['__fields']])
		# log.debug(None, "Props are %s" % props)
		return self.__class__(self.__model, self.__table, **props)
	
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
				vals.append((self.__dict__[f] if not isinstance(self.__dict__[f], PotentialModelInstance) else self.__dict__[f].id))
		m = lambda x: "'%s'" % x;
		r = lambda a, v: "%s, %s" % (a,v);
		cols_vals = (reduce(r, map(m, cols)), reduce(r, map(m, vals)))
		query = "INSERT INTO " + self.__table + ("(%s) VALUES (%s);" % cols_vals)
		# print "Executing " + query
		self.id = self.__model.execute_insert(query)
	
	def _update(self):
		query = "UPDATE %s SET " % self.__table
		for f in self.__class__.__dict__['__fields']:
			if self.__dict__.has_key(f) and not f == 'id':
				query += "%s='%s'," % (f, self.__dict__[f])
		query = query[:-1] + " WHERE id = '%s'" % self.id
		# print query
		print self.__model.execute_insert(query)