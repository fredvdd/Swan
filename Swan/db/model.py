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
	
	def set_pool(self, pool):
		self.__class__.pool = pool
		return pool
		
	def execute_query(self, query):
		worker = self.workers.one()
		cols, rows = worker.execute(query)
		props = [dict(zip([col[0] for col in cols],row))for row in rows]
		return [self.model_instance(**ps) for ps in props]
	
	@classmethod
	def all(cls):
		return Query(cls.pool.one(), cls.__name__, **{})
	
	@classmethod
	def filter(cls, **kwds):
		return Query(cls.pool.one(), cls.__name__, **kwds)
	
	@classmethod
	def get(cls, **kwds):
		return SingleQuery(cls.pool.one(), cls.__name__, cls.instance_type, **kwds)
		
class ModelInstance(object):
	
	def __init__(self, **props):
		self.__dict__.update(props)