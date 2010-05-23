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
		results = self.model.execute_select(query)
		return results
		
	def __iter__(self):
		if not self.cached:
			self.cache = self._evaluate()
			self.cached = True
		return iter(self.cache)

	def __repr__(self):
		if not self.cached:
			self.cache = self._evaluate()
			self.cached = True
		return str(self.cache)
		
class SingleQuery(Query):
	
	def __init__(self, model, table, instance_type, **filters):
		self.instance_type = instance_type
		Query.__init__(self, model, table, **filters)
		
	def evaluate(self):
		return Query._evaluate(self)[0]
		
	def __getattr__(self, name):
		if hasattr(self.instance_type, name) and isinstance(self.instance_type.__dict__[name], ForeignRelation): 
			return RelationSet(self.instance_type.__dict__[name],self.model, self.table, **self.filters)
		if not object.__getattribute__(self, 'cached'):
			self.cache = self.evaluate()
		v = getattr(self.cache, name)
		return v
		#return object.__getattribute__(self, name)
		
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
	
	def add(self, **props):
		if not self.join_instance:
			self.join_instance = self.join_model.execute_select(Query._build_query_string(self, self.join_table))[0];
		props.update({self.join_col:self.join_instance.id})
		return self.relation.create(**props)

class ForeignRelation(object):
	
	def __init__(self, name, table, col):
		self.name = name
		self.table = table
		self.col = col
		
	def __str__(self):
		return "%s:%s" % (self.table, self.col)


def equals(value):
	return "= '%s'" % value
	
def less_than(value):
	return "< %s" % value

def greater_than(value):
	return "> %s" % value