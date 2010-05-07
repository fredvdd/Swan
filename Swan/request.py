from Actors.keywords import *
from BaseHTTPServer import BaseHTTPRequestHandler
from time import time, gmtime


class Request(object):
	
	def __init__(self, parent, socket, rfile, wfile, method, path, headers, params):
		self.parent = parent
		self.socket = socket
		self.wfile = wfile
		self.rfile = rfile
		self.method = method
		self.path = path
		self.headers = headers
		self.params = params
		
	def __str__(self):
		return "request for %s" % self.path
	
	def start_response(self):
		return Response(self, self.wfile)
		
	def try_repeat(self):
		if self.headers.has_key('Connection') and self.headers['Connection'] == 'close':
			self.socket.close()
		else:
			self.parent.handle_request(self.socket, self.rfile, self.wfile)
			
	def get_body(self):
		length = self.headers['Content-length']
		content = self.rfile.read(length)
		return content

class Response(object):
	
	def __init__(self, partner, wfile):
		self.partner = partner
		self.wfile = wfile

	def send(self):
		self.wfile.flush()
		self.partner.try_repeat()
		
	def and_content(self, string):
		self.and_header("Content-length", len(string))
		self.wfile.write("\r\n")
		self.wfile.write(string)
		return self
	
	def with_status(self, code):
		name, message = BaseHTTPRequestHandler.responses[code]
		self.wfile.write("HTTP/1.1 %s %s\n" % (code, name))
		self.date_header()
		self.connection_header()
		return self
	
	def with_content_type(self, ctype):
		return self.and_header("Content-type", ctype)
	
	def and_header(self, key, value):
		self.wfile.write("%s:%s\n" % (key,value))
		return self
	
	def and_headers(self, headers):
		try:
			l = headers.iteritems()
		except AttributeError:
			l = header_dict
		for k, v in l:
			self.and_header(k, v)
		return self
		
	def connection_header(self):
		if not self.partner.headers.has_key('Connection'):
		 	connection = "close"
		else:
			 connection = self.partner.headers['Connection']
		self.and_header('Connection', connection)
		
	def date_header(self):
		timestamp = time()
		year, month, day, hh, mm, ss, wd, y, z = gmtime(timestamp)
		datetime = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
		self.and_header("Date", datetime)
	
	weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	
	def with_error(self, error_code, message):
		return ErrorResponse(self.partner, self.wfile, error_code, message)

class ErrorResponse(Response):
	
	def __init__(self, partner, wfile, code, message):
		Response.__init__(self, partner, wfile)
		name, more = BaseHTTPRequestHandler.responses[code]
		self.content = 	"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
		<html><head>
		<title>%(code)d %(name)s</title>
		</head><body>
		<h1>%(name)s</h1>
		<p>%(more)s</p>
		<p>%(message)s</p>
		<hr>
		<address>Swan/0.1 (OSX) Server at localhost on port 8080</address>
		</body></html>
		"""	% {'code': code, 'name' : name, 'more': more, 'message': message}
		
		self.wfile.write("HTTP/1.1 %s %s\n" % (code, name))
		self.date_header()
		self.and_headers({
			"Content-type": "text/html",
			"Connection": "close",
			"Content-Length": len(self.content)
		})
	
	def send(self):
		self.wfile.write(self.content)
		Response.send(self)
		