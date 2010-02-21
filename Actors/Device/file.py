from Actors.keywords import *

class File(MobileActor):

	def birth(self):
		pass
		
	def read(self, filepath, size=-1):
		try:
			self.file = open(filepath, 'r')
			res = self.file.read(size)
			self.file.close()
			return res
		except IOError:
			return ""
