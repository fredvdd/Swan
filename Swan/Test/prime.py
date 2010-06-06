from Actors.keywords import *
import math

class PrimeFinder(LocalActor):
	
	def birth(self):
		self.highest = 2
		while self.highest > 0:
			print "%s, " % self.highest,
			self.highest = self.nextPrime(self.highest+1)
	
	def get_highest(self):
		return self.highest
		
	def nextPrime(self, next):
		return next if self.isPrime(next,2) else self.nextPrime(next+1)
	
	def isPrime(self, test, div):
		while div <= test/div:
			if test % div == 0:
				return False
			div+=1
		return True
			

def start():
	PrimeFinder()

if __name__ == '__main__':
	initialise(start)