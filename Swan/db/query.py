from Actors.keywords import *
from Swan.db.constraints import Constraint
from Swan.static import log

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
		
	def _build_query_string(self, table):
		query = "SELECT * FROM " + table
		if len(self.filters) < 1:
			return query
		return query + " WHERE " + reduce(lambda s, (p,v): "%s %s AND %s" % (p,v,s), self.filters.iteritems(), "")[:-4]
		
	def _evaluate(self):
		query = self._build_query_string(self.table)
		# log.debug(None, "Evaluating %s" % query)
		results = self.model.execute_select(query)
		return results
		
	def _check_cache(self):
		if not self.cached:
			# print "Filling cache with filters %s" % self.filters
			self.cache = self._evaluate()
			self.cached = True
		
	def __iter__(self):
		self._check_cache()
		return iter(self.cache)

	def __repr__(self):
		self._check_cache()
		return str(self.cache)
		
	def __len__(self):
		self._check_cache()
		return len(self.cache)
	
	def __getitem__(self,key):
		self._check_cache()
		return self.cache[key]
		
	def __deepcopy__(self,memo):
		return Query(self.model.__deepcopy__(memo), self.table, **self.filters)
	
	def __getstate__(self):
		return (self.model, self.table, self.filters, self.cache, self.cached)
	
	def __setstate__(self, state):
		self.model, self.table, self.filters, self.cache, self.cached = state
		
class RelationSet(Query):
	
	def __init__(self, relation, join_model, join_table, **filters):
		self.relation, self.join_col = (relation.table, relation.col)
		self.join_model = join_model
		self.join_table = join_table
		Query.__init__(self, self.relation.pool.one(), relation.name, **filters)
		self.join_instance = None
		
	def _build_query_string(self, table):
		t, j, c = (self.table, self.join_table, self.join_col)
		fields = self.relation.instance_type.__dict__['__fields']
		selection = reduce(lambda s, k: "%s, %s" % (s,k), [f for f in fields if not f =='id'], t + ".id")
		query = "SELECT %s FROM %s, %s WHERE %s.%s = %s.id" % (selection, t, j, t, c, j)
		query += " AND " + reduce(lambda s, (p,v): "%s.%s %s AND %s" % (self.join_table,p,v,s), self.filters.iteritems(), "")[:-4]
		return query
		
	def __repr__(self):
		return Query.__repr__(self)
		
	def __iter__(self):
		# log.debug(None, "Getting relation set iter")
		return Query.__iter__(self)
	
	def __getitem__(self, key):
		# print "Getitem"
		return Query.__getitem__(self, key)
	
	def add(self, **props):
		# print "Adding %s" % props
		if not self.join_instance:
			self.join_instance = self.join_model.execute_select(Query._build_query_string(self, self.join_table))[0];
		props.update({self.join_col:self.join_instance.id})
		# print "Props now %s" % props
		return self.relation.create(**props)
	
	def delete(self, **props):
		params = map(lambda (k,v): "%s %s" % (k, v if isinstance(v,Contstraint) else ("=%s"%v)), props.iteritems())
		print "Delete params %s" % params
		# self.relation.execute_insert("")