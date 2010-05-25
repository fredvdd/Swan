from Actors.keywords import *

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
		# print "Evaluating %s" % query
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
		
class SingleQuery(Query):
	
	def __init__(self, model, table, instance_type, **filters):
		# print "Single Query: %s, %s, %s, %s" % (model, table, instance_type, filters)
		self.instance_type = instance_type
		Query.__init__(self, model, table, **filters)
		
	def evaluate(self):
		return Query._evaluate(self)[0]
		
	# def __getattr__(self, name):
	# 	print "Get attr %s, %s" % (name, dir(self.instance_type))
	# 	if hasattr(self.instance_type, name) and isinstance(self.instance_type.__dict__[name], ForeignRelation): 
	# 		return RelationSet(self.instance_type.__dict__[name],self.model, self.table, **self.filters)
	# 	if hasattr(self.instance_type, name) or self.instance_type.__dict__['__fields'].has_key(name):
	# 		print "asdfsdf"
	# 		if not object.__getattribute__(self, 'cached'):
	# 			self.cache = self.evaluate()
	# 		v = getattr(self.cache, name)
	# 		return v
	# 	# try:
	# 	return object.__getattribute__(self, name)
		# except AttributeError:
		# 	print "SingleQuery has no attribute %s" % name
		# 	if not object.__getattribute__(self, 'cached'):
		# 		self.cache = self.evaluate()
		# 	v = getattr(self.cache, name)
		# 	return v
		#return object.__getattribute__(self, name)
	
	def __getattribute__(self, name):
		it = object.__getattribute__(self,'instance_type')
		if hasattr(it,name) or it.__dict__['__fields'].has_key(name):
			if it.__dict__.has_key(name) and isinstance(it.__dict__[name], ForeignRelation):
				return RelationSet(it.__dict__[name],object.__getattribute__(self, 'model'), object.__getattribute__(self,'table'), **object.__getattribute__(self, 'filters'))
			if not object.__getattribute__(self, 'cached'):
				object.__setattr__(self, 'cache', object.__getattribute__(self, 'evaluate')())
				object.__setattr__(self, 'cached', True)
			return object.__getattribute__(self.cache,name)
		return object.__getattribute__(self,name)
		
	def __deepcopy__(self, memo):
		return SingleQuery(self.model.__deepcopy__(memo), self.table, self.instance_type, **self.filters)
	
	def __getstate__(self):
		return (self.model, self.table, self.filters, self.instance_type)
	
	def __setstate__(self, state):
		self.model, self.table, self.filters, self.instance_type = state
		self.cache = []
		self.cached = False
		
class RelationSet(Query):
	
	def __init__(self, relation, join_model, join_table, **filters):
		self.relation, self.join_col = (relation.table, relation.col)
		self.join_model = join_model
		self.join_table = join_table
		Query.__init__(self, self.relation.pool.one(), relation.name, **filters)
		self.join_instance = None
		
	def _build_query_string(self, table):
		t, j, c = (self.table, self.join_table, self.join_col)
		query = "SELECT * FROM %s, %s WHERE %s.%s = %s.id" % (t, j, t, c, j)
		query += " AND " + reduce(lambda s, (p,v): "%s.%s %s AND %s" % (self.join_table,p,v,s), self.filters.iteritems(), "")[:-4]
		return query
		
	def __repr__(self):
		return Query.__repr__(self)
		
	def __iter__(self):
		return Query.__repr__(self)
	
	def __getitem__(self, key):
		# print "Getitem"
		return Query.__getitem__(self, key)
	
	def add(self, **props):
		if not self.join_instance:
			self.join_instance = self.join_model.execute_select(Query._build_query_string(self, self.join_table))[0];
		props.update({self.join_col:self.join_instance.id})
		return self.relation.create(**props)

class ForeignRelation(object):
	
	def __init__(self, *args):
		self.name, self.table, self.col, self.join_name, self.join_table = args
		
	def __str__(self):
		return "%s:%s joins to %s:id" % (self.name, self.col, self.join_name)


def equals(value):
	return "= '%s'" % value
	
def less_than(value):
	return "< %s" % value

def greater_than(value):
	return "> %s" % value