from Actors.keywords import *

class LazyActor(MobileActor):
	
	def birth(self):
		print "Lazy Actor"
		
	def send(self, lst):
		self.list = lst
	
	def iterator(self):
		return [2*x for x in self.list]
		
class TestActor(MobileActor):
	
	def birth(self, la):
		la.send([1,2,3,4])
		for x in la:
			print x,


def start():
	la = LazyActor()
	TestActor(la)

if __name__ == '__main__':
    initialise(start)