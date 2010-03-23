from classes import Test4 as T4
import function, listcomp as lc

class Test5(T4):
	
	def __init__(self):
		self.fun = True
m = Manager()
a = T4()
b = function.return_(4,5)
c = Test5()
print a.test(5,6)
print b