from Actors.keywords import *
from fields import IntegerField, ForeignKey
from query import Query, RelationSet
from relation import ForeignRelation
from constraints import equals
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
		return [self.model_instance(self, self.__class__, **ps) for ps in props]
	
	def execute_insert(self, query):
		log.debug(self, "Executing SQL: " + query)
		cursor = self.workers.one().get_cursor()
		cursor.execute(query)
		return cursor.lastrowid()
	
	@classmethod
	def all(cls):
		return Query(cls.pool.one(), cls, **{})
	
	@classmethod
	def filter(cls, **kwds):
		return Query(cls.pool.one(), cls, **kwds)
	
	@classmethod
	def get(cls, **kwds):
		return PotentialModelInstance(cls.pool.one(), cls, **kwds)
		
	@classmethod
	def create(cls, **kwds):
		# print "Creating %s with %s" % (cls.instance_type.__name__, kwds)
		return cls.instance_type(cls.pool.one(), cls, **kwds)
		
class PotentialModelInstance(Query):

	def __init__(self, model, model_type, **filters):
		# print "Single Query: %s, %s, %s, %s" % (model, table, instance_type, filters)
		self.model_type = model_type
		Query.__init__(self, model, model_type, **filters)

	def _check_cache(self):
		if not self.cached:
			# print "Filling cache with filters %s" % self.filters
			self.cache = self._evaluate()[0]
			self.cached = True

	def __getattribute__(self, name):
			try:
				# print "Get %s attr from %s" % (name, object.__getattribute__(self, '__class__'))
				if name not in ['__repr__','__len__', '__iter__', '__getitem__']:
					return object.__getattribute__(self, name)
				else:
					raise AttributeError
			except AttributeError:
				it = object.__getattribute__(self,'instance_type')
				if hasattr(it,name) or it.__dict__['__fields'].has_key(name):
					if it.__dict__.has_key(name) and isinstance(it.__dict__[name], ForeignRelation):
						return RelationSet(it.__dict__[name],object.__getattribute__(self, 'model'), object.__getattribute__(self,'model_type'), **object.__getattribute__(self, 'filters'))
				if not object.__getattribute__(self, 'cached'):
					log.debug(None, "Getting cache for %s access" % name)
					object.__getattribute__(self, '_check_cache')()
					# object.__setattr__(self, 'cache', object.__getattribute__(self, 'evaluate')())
					# object.__setattr__(self, 'cached', True)
					return getattr(object.__getattribute__(self,'cache'),name)
		# return object.__getattribute__(self,name)

	def __deepcopy__(self, memo):
		return PotentialModelInstance(self.model.__deepcopy__(memo), self.model_type, **self.filters)

	def __getstate__(self):
		return (self.model, self.table, self.model_type, self.instance_type, self.filters, self.cache, self.cached)

	def __setstate__(self, state):
		self.model, self.table, self.model_type, self.instance_type, self.filters, self.cache, self.cached = state
		
class ModelInstance(object):
	__fields = None
	
	def __init__(self, model, model_type, **props):
		# log.debug(None, "Creating %s with props %s" % (self.__class__.__name__, props))
		self.__model = model
		self.__table = model_type.__name__ if hasattr(model_type, '__name__') else model_type
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
						self.__dict__[f] = rtable.get(id=equals(props[f]))
			elif f == 'id':
				self.__dict__[f] = props[f] if props.has_key(f) else (props[self.__table+'.id'] if props.has_key(self.__table+'.id') else None)
			else:
				self.__dict__[f] = props[f] if props.has_key(f) else None;
		# log.debug(None, self.__dict__.has_key('id'))

	# def __getattribute__(self, name):
	# 	attr = object.__getattribute__(self, name)
	# 	if isinstance(attr, PotentialModelInstance):
	# 		log.debug(object.__getattribute__(self, '__class__').__name__, "asked for PotentialModelInstance attribute %s" % name)
	# 		
	# 	return attr
	
	def __deepcopy__(self, memo):
		props = dict([(f,self.__dict__[f]) for f in self.__class__.__dict__['__fields']])
		return self.__class__(self.__model, self.__table, **props)
	
	def __getstate__(self):
		return (self.__model, self.__table) + tuple([(f,self.__dict__[f]) for f in self.__class__.__dict__['__fields']])
		
	def __setstate__(self,state):
		self.__model, self.__table = state[:2]
		self.__dict__.update(dict(state[2:]))
		
	def save(self):
		if hasattr(self,"id") and not self.id == None:
			self._update()
		else:
			self._insert()
		return self
	
	def _insert(self):
		cols = list()
		vals = list()
		for f in self.__class__.__dict__['__fields']:
			if self.__dict__.has_key(f) and not self.__dict__[f] == None:
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