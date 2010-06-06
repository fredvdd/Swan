from Actors.keywords import *
from httplib import HTTPConnection, HTTPResponse

class HTTP(MobileActor):
	
	def birth(self):
		self.connections = dict()
		self.ids = 0
	
	def connect(self, server, port=80):
		conn = HTTPConnection(server, port)
		self.ids += 1
		self.connections[self.ids] = conn
		return HTTPReference(self, self.ids)
	
	def _http_call(self, conn_id, name, args, kwds):
		print "Calling %s on connection %s with args %s and kwds %s" % (name, conn_id, args, kwds)
		meth = getattr(self.connections[conn_id],name)
		print "Method is %s" % meth
		result = meth(*args, **kwds)
		if isinstance(result, HTTPResponse):
			result = StageHTTPResponse(result)
		return result


class HTTPReference(object):
	
	def __init__(self, actor_id, conn_id):
		self.actor_id = actor_id
		self.conn_id = conn_id
		
	def __deepcopy__(self, memo):
		return HTTPReference(self.actor_id, self.conn_id)
	
	def __getstate__(self):
		return (self.actor_id, self.conn_id)

	def __setstate__(self, state):
		self.actor_id, self.conn_id = state
		
	def __str__(self):
		return "HTTP Reference %s " % self.actor_id
		
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		return HTTPReferenceCall(self.actor_id, self.conn_id, name)
		
	def get(self, url):
		return self.actor_id._http_call(self.conn_id, 'request', ('GET',url), {})
	

class HTTPReferenceCall(object):
	
	def __init__(self, actor, conn_id, method):
		self.actor = actor
		self.conn_id = conn_id
		self.method = method
	
	def __call__(self, *args, **kwds):
		return self.actor._http_call(self.conn_id, self.method, args, kwds)
		
class StageHTTPResponse(object):
	
	def __init__(self, r):
		self.body = r.read()
		self.headers = dict(r.getheaders())
		self.msg, self.version, self.status, self.reason = r.msg, r.version, r.status, r.reason
		
	def __deepcopy__(self, memo):
		shr = object.__new__(StageHTTPResponse)
		shr.__dict__.update(self.__dict__)
		return shr
	
	def __getstate__(self):
		return (self.body, self.headers, self.msg, self.version, self.status, self.reason)
		
	def __setstate__(self, state):
		self.body, self.headers, self.msg, self.version, self.status, self.reason = state
		
	def read(self):
		return self.body
	
	def getheader(self,name, default=None):
		return self.headers[name] if self.headers.has_key(name) else default
	
	def getheaders(self):
		return self.headers.items()