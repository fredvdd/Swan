from Actors.keywords import *
from Actors.Device.file import File

class FileHandler(MobileActor):

	def birth(self, root):
		print "FileHandler created!"

	def get(self, path):
		result = ("%s %d %s\r\n" % ("HTTP/1.1", 200, "OK"))
		result += ("%s: %s\r\n" % ("Content-type", "text/html"))
		result += "\r\n"
		return result + File(root+path).read()  
