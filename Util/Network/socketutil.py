import sys
import socket
import rpc

def server_socket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen(5)
    return sock
    
def client_socket():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock 
	
class SocketReference(object):

	def __init__(self, manager_loc, socket_id):
		print "SocketReference for %s" % socket_id
		self.__manager_loc = manager_loc
		self.__socket_id = socket_id

	def __getattr__(self, name):
		print "Get Atrribute %s" % name
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		else:
			return SocketRequest(self.__socket_id, self.__manager_loc, name)
			
	def __deepcopy__(self, memo):
		return SocketReference(self.__manager_loc, self.__socket_id)

	def __getstate__(self):
		return (self.__manager_loc, self.__socket_id)

	def __setstate__(self, state):
		self.__manager_loc = state[0]
		self.__socket_id = state[1]

	def __str__(self):
	 return "Reference for %s on %s" % (self.__socket_id, self.__manager_loc)


class SocketRequest(object):

	def __init__(self, socket_id, manager_loc, method):
		self.socket_id = socket_id
		self.manager_loc = manager_loc
		self.method = method

	def __call__(self, *args, **kwds):
		network_locator = rpc.RPCConnector(self.manager_loc)
		manager = network_locator.connect()
		return manager.socket_call(self.socket_id, self.method,  *args, **kwds)