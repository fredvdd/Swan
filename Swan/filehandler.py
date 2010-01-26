from Actors.keywords import *
from Actors.Device.file import File
from BaseHTTPServer import BaseHTTPRequestHandler

class FileHandler(MobileActor):

	def birth(self, root):
		print "FileHandler created!"
		self.root = root
		
	def get(self, path):
		content = File(self.root+path).read()
		if content:
			result = ("%s %d %s\r\n" % ("HTTP/1.1", 200, "OK"))
			result += ("%s: %s\r\n" % ("Content-type", "text/html"))
			result += "\r\n"
			return result +  content 
		else:
			return self.http_error(404, "The file %s was not found" % path)
	
	def http_error(self, code, message=None):
		name, more = BaseHTTPRequestHandler.responses[code]
		if not message:
			message = more
		result = ("%s %d %s\r\n" % ("HTTP/1.1", code, name))
		result += ("%s: %s\r\n" % ("Content-type", "text/html"))
		result += ("%s: %s\r\n" % ("Connection", "close"))
		result += "\r\n"
		result += ("""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
		<html><head>
		<title>%(code)d %(name)s</title>
		</head><body>
		<h1>%(name)s</h1>
		<p>%(message)s</p>
		<p>Additionally, a 404 Not Found
		error was encountered while trying to use an ErrorDocument to handle the request.</p>
		<hr>
		<address>Apache/2.2.14 (Unix) mod_ssl/2.2.14 Server at katherinethomas.co.uk Port 80</address>
		</body></html>
		""" % {'code': code, 'name':name, 'message': message, 'more': more})
		return result