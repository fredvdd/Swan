import sys
import socket
import rpc

def server_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen(512)
    return sock
    
def client_socket():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock 
	
class SocketReference(object):

	def __init__(self, manager_loc, socket_id):
		self.manager_loc = manager_loc
		self.socket_id = socket_id

	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		else:
			return SocketRequest(self.socket_id, self.manager_loc, "sock:%s" % name)
			
	def __deepcopy__(self, memo):
		return SocketReference(self.manager_loc, self.socket_id)

	def __getstate__(self):
		return (self.manager_loc, self.socket_id)

	def __setstate__(self, state):
		self.manager_loc, self.socket_id = state
		
	def __str__(self):
	 return "Reference for %s on %s" % (self.socket_id, self.manager_loc)
	
class SocketFileReference(object):
	
	def __init__(self, manager_loc, socket_id, mode):
		self.manager_loc = manager_loc
		self.socket_id = socket_id
		self.mode = mode
	
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		else:
			return SocketRequest(self.socket_id, self.manager_loc, "%sfile:%s" % (self.mode, name))
			
	def __deepcopy__(self, memo):
		return SocketFileReference(self.manager_loc, self.socket_id, self.mode)

	def __getstate__(self):
		return (self.manager_loc, self.socket_id, self.mode)

	def __setstate__(self, state):
		self.manager_loc, self.socket_id, self.mode = state
				
	def __str__(self):
		return "File reference for %s on %s (mode %s)" % (self.socket_id, self.manager_loc, self.mode)
		
class SocketRequest(object):

	def __init__(self, socket_id, manager_loc, method):
		self.socket_id = socket_id
		self.manager_loc = manager_loc
		self.method = method

	def __call__(self, *args, **kwds):
		network_locator = rpc.RPCConnector(self.manager_loc)
		manager = network_locator.connect()
		res = manager.socket_call(self.socket_id, self.method,  *args, **kwds)
		res = None if res == "NONE" else res
		return res