class ForeignRelation(object):

	def __init__(self, *args):
		self.name, self.table, self.col, self.join_name, self.join_table = args

	def __str__(self):
		return "%s:%s joins to %s:id" % (self.name, self.col, self.join_name)

	def __deepcopy__(self, memo):
		return ForeignRelation(self.name, self.table, self.col, self.join_name, self.join_table)

	def __getstate__(self):
		return (self.name, self.table, self.col, self.join_name, self.join_table)

	def __setstate__(self, state):
		(self.name, self.table, self.col, self.join_name, self.join_table) = state