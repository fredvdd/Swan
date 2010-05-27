from Actors.keywords import *
from BaseHTTPServer import BaseHTTPRequestHandler
from time import time, gmtime
from json import JSONEncoder, dumps, loads
from Swan.coding import encoders, decoders, PassThroughEncoder, PassThroughDecoder

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
		self.body = None
		
	def __str__(self):
		return "request for %s" % self.path
	
	def start_response(self):
		return Response(self, self.wfile)
		
	def try_repeat(self):
		if self.headers.has_key('Connection') and self.headers['Connection'] != 'close':
			self.parent.handle_request(self.socket, self.rfile, self.wfile)
		else:
			self.socket.close()
			
	def get_body(self):
		if self.body:
			return self.body
		length = self.headers['Content-length']
		self.body = self.decode(self.headers['Content-type'], self.rfile.read(int(length)))
		return self.body
		
	
	def decode(self, content_type, content):
		return decoders.get(content_type, PassThroughDecoder)().get_decoding(content)

class Response(object):
	
	def __init__(self, partner, wfile):
		self.partner = partner
		self.wfile = wfile
		self.headers = dict()
		self.code=None
		self.name=None
		self.content=None

	def send(self, status_code=None, content=None, content_type=None):
		if status_code:
			self.with_status(status_code)
		if content and content_type:
			self.with_content(content, content_type)
			
		self.wfile.write("HTTP/1.1 %s %s\n" % (self.code, self.name))
		for k,v in self.headers.iteritems():
			self.wfile.write("%s:%s\n" % (k,v))
		self.wfile.write(("\r\n%s" % self.content) if self.content else "")
		self.wfile.flush()
		self.partner.try_repeat()
		
	def with_content(self, content, content_type=None):
		if content_type:
			self.with_content_type(content_type)
		content_str=self.encode(self.content_type, content)
		self.content = content_str
		self.headers["Content-length"] = len(content_str)
		# self.wfile.write("%s:%s\n" % ("Content-length", len(content_str)))
		# self.wfile.write("\r\n")
		# self.wfile.write(content_str)
		return self
	
	def with_status(self, code):
		name, message = BaseHTTPRequestHandler.responses[code]
		self.code = code
		self.name = name
		# self.wfile.write("HTTP/1.1 %s %s\n" % (code, name))
		self.date_header()
		self.connection_header()
		return self
	
	def with_content_type(self, ctype):
		self.content_type = ctype
		return self.with_header("Content-type", ctype)
	
	def with_header(self, key, value):
		# self.wfile.write("%s:%s\n" % (key,value))
		# self.headers.update({key:value})
		self.headers[key] = value
		return self
	
	def with_headers(self, **headers):
		self.headers.update(headers)
		# for k, v in headers.iteritems():
		# 	self.with_header(k, v)
		return self
		
	def connection_header(self):
		if not self.partner.headers.has_key('Connection'):
		 	connection = "close"
		else:
			 connection = self.partner.headers['Connection']
		self.with_header('Connection', connection)
		
	def date_header(self):
		timestamp = time()
		year, month, day, hh, mm, ss, wd, y, z = gmtime(timestamp)
		datetime = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
		self.with_header("Date", datetime)
	
	weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	
	def send_error(self, error_code, message):
		return ErrorResponse(self.partner, self.wfile, error_code, message)

	def encode(self, content_type, content):
		return encoders.get(content_type, PassThroughEncoder)().get_encoding(content)

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
		self.with_headers(**{
			"Content-type": "text/html",
			"Connection": "close",
			"Content-Length": len(self.content)
		})
	
	def send(self):
		self.wfile.write(self.content)
		self.wfile.flush()
		self.partner.try_repeat()
		# Response.send(self)
		