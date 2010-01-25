from Actors.keywords import *

class File(MobileActor):

	def birth(self, filepath, mode='r'):
		self.filepath = filepath
		self.mode = mode
		
	
	def read(self, size=-1):
		self.file = open(filepath, mode)
		res = self.file.read(size)
		self.file.close()
		return res
