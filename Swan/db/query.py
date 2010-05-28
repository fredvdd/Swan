from Actors.keywords import *
from constraints import Constraint
from relation import ForeignRelation
from Swan.db import log

class Query(object):
	
	def __init__(self, model, table, instance_type, **filters):
		self.model = model
		self.table = table
		self.instance_type = instance_type
		self.filters = filters
		self.cache = []
		self.cached= False

	def filter(self, **filters):
		temp_filters = self.filters
		temp_filters.update(filters)
		return Query(self.model, self.table, **temp_filters)
		
	def _build_query_string(self, table):
		cols = [f for f in getattr(self.instance_type, '__fields')]
		query = "SELECT * FROM " + table
		if len(self.filters) < 1:
			return query
		return (cols, query + " WHERE " + reduce(lambda s, (p,v): "%s %s AND %s" % (p,v,s), self.filters.iteritems(), "")[:-4])
		
	def _evaluate(self):
		desc, query = self._build_query_string(self.table)
		log.debug(None, "Evaluating %s" % query)
		results = self.model.execute_select(desc, query)
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
		Query.__init__(self, self.relation.pool.one(), relation.name, self.relation.instance_type, **filters)
		self.join_instance = None
		
	def _build_query_string(self, table):
		t, j, c = (self.table, self.join_table, self.join_col)
		fields = getattr(self.relation.instance_type, '__fields')
		selection = self._compress(map(self._process_field, fields.iteritems()), [])
		# print selection
		selstr = reduce(lambda a, s: "%s, %s" %(a,s), selection)
		query = "SELECT %s FROM %s, %s WHERE %s.%s = %s.id" % (selstr, t, j, t, c, j)
		query += " AND " + reduce(lambda s, (p,v): "%s.%s %s AND %s" % (self.join_table,p,v,s), self.filters.iteritems(), "")[:-4]
		# print query
		return (selection, query)
		
	def _compress(self, sellist, acc):
		if len(sellist) == 0:
			return acc
		head, tail = (sellist[0], sellist[1:])
		if hasattr(head, '__iter__'):
			return self._compress(head, acc) + self._compress(tail, acc)
		else:
			return [head] + self._compress(tail, acc)
		
	
	def _process_field(self, field):
		fname, ftype = field
		if fname == 'id':
			return self.table + ".id"
		if fname == self.join_col and isinstance(ftype, ForeignRelation):
			return map(lambda x: "%s.%s" %(ftype.join_name,x), getattr(ftype.join_table.instance_type, '__fields'))
		return fname
		
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
		params = map(lambda (k,v): "%s %s" % (k, v if isinstance(v,Constraint) else ("= %s"%v)), props.iteritems())
		paramstr = reduce(lambda a,p:"%s, %s" % (a,p), params)
		print "Delete params %s" % paramstr
		query = "DELETE FROM %s WHERE %s" % (self.table, paramstr)
		print query
		print self.model.execute_insert(query)
		# self.relation.execute_insert("")