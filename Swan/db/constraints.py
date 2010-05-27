class Constraint(object):
	
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return self.compile()
	
	def compile(self):
		pass
		
class EqualConstraint(Constraint):
	
	def compile(self):
		return "= '%s'" % self.value
		
class LessThanConstraint(Constraint):

	def compile(self):
		return "< '%s'" % self.value
		
class GreaterThanConstraint(Constraint):

	def compile(self):
		return "> '%s'" % self.value

def equals(value):
	return EqualConstraint(value)
	
def less_than(value):
	return LessThanConstraint

def greater_than(value):
	return GreaterThanConstraint(value)