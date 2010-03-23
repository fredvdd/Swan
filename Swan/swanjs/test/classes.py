class Test():
	pass

class Test2:
	def __init__(self):
		self.fun = True #no really
	
	def add(self, a, b):
		return a + b

class Test3:
	field1 = "one"
	field2 = "two"
	
class Test4(Test2):
	def __init__(self):
		self.fun = False
	
	def test(self, a, b):
		if self.add(a,b) and self.fun:
			return "alpha"
		else:
			return "beta"

# a = Test4()
# print a.test(5,6)