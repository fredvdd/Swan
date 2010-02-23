class Person(object):
	
	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def say_hello(self):
		print "Hello from " + self.name + ", age " + str(self.age)
	

if __name__ == '__main__':
	normalperson = Person("Rob", 22)
	normalperson.say_hello()
	weirdperson = object.__new__(Person)
	weirdperson.__dict__ = dict(name="Fred", age=22)
	weirdperson.say_hello()