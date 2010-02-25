class Base(object):
	
	def __new__(cls):
		super_class = super(Base, cls).__new__(cls)
		# for (x,y) in cls.__dict__.iteritems():
		# 	print str(x) + " ->\t" + str(y)
		# print cls.__name__
		return super_class
	
	def __init__(self):
		print "Created"
		print self.__class__.__dict__
		
class More(Base):
	field = "GOld"
	
	def __init__(self):
		Base.__init__(self)
		#print self.__class__
		#print "Recreated"


if __name__ == '__main__':
	b = More()
