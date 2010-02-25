from Actors.keywords import *
from BaseHTTPServer import BaseHTTPRequestHandler
from time import time, gmtime


class Request(object):
	
	def __init__(self, parent, socket, rfile, wfile, path, headers, params):
		self.parent = parent
		self.socket = socket
		self.wfile = wfile
		self.rfile = rfile
		self.path = path
		self.headers = headers
		self.params = params
		
	def __str__(self):
		return "request for %s" % self.path
	
	def start_response(self):
		return Response(self, self.wfile, )
		
	def try_repeat(self):
		if self.headers.has_key('Connection') and self.headers['Connection'] == 'close':
			self.socket.close()
		else:
			#print "not closing connection"
			self.parent.handle_request(self.socket, self.rfile, self.wfile)

class Response(object):
	
	def __init__(self, partner, wfile):
		self.partner = partner
		self.wfile = wfile

	def done(self):
		self.wfile.flush()
		self.partner.try_repeat()
		
	def send(self, string):
		self.wfile.write(string)
		return self
	
	def set_status(self, code):
		name, message = BaseHTTPRequestHandler.responses[code]
		self.wfile.write("HTTP/1.1 %s %s\n" % (code, name))
		self.date_header()
		return self
	
	def set_header(self, key, value):
		self.wfile.write("%s:%s\n" % (key,value))
		return self
	
	def set_headers(self, header_dict):
		for k, v in header_dict:
			self.set_header(k, v)
		return self
	
	def end_headers(self):
		self.wfile.write("\r\n")
		return self
		
	def date_header(self):
		timestamp = time()
		year, month, day, hh, mm, ss, wd, y, z = gmtime(timestamp)
		datetime = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
		self.set_header("Date", datetime)
	
	weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	
	def send_error(self, error_code, message):
		name, more = BaseHTTPRequestHandler.responses[error_code]
		content = 	"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
		<html><head>
		<title>%(code)d %(name)s</title>
		</head><body>
		<h1>%(name)s</h1>
		<p>%(more)s</p>
		<p>%(message)s</p>
		<hr>
		<address>Swan/0.1 (OSX) Server at localhost on port 8080</address>
		</body></html>
		"""	% {'code': error_code, 'name' : name, 'more': more, 'message': message}
		
		self.wfile.write("HTTP/1.1 %s %s" % (error_code, name))
		self.set_headers([
			("Content-type", "text/html"),
			("Connection", "close"),
			("Content-Length", len(content))
		]).end_headers().send(content).done()
		