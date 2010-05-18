
class Field(object):
	fieldtype = ''
	def field_type(self):
		return self.fieldtype
	
class IntegerField(Field):
	fieldtype = 'integer'
	pass
	
class TextField(Field):
	fieldtype = 'varchar'
	
	def __init__(self, maxlength=256):
		self.max = maxlength
		
	def field_type(self):
		return "%s(%s)" % (self.fieldtype, self.max)
	
class EmailField(TextField):
	
	def __init__(self, maxlength=256):
		TextField.__init__(self, maxlength)

class TimeField(Field):
	fieldtype = 'timestamp'

class ForeignKey(Field):
	
	def __init__(self, table):
		self.table = table
		
	def field_type(self):
		return 'integer not null references "%s"("id")' % (self.table)