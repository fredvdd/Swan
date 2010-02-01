import threading
from Util.Network import socketutil, rpc
from Manager.managerlog import log

class SocketStore(object):
	def __init__(self, overlay):
		self.__overlay = overlay
		self.__socket_lock = threading.Lock()
		self.sockets = {}
	
	def add_socket(self, socket_id, handler):
		with self.__socket_lock:
			self.sockets[socket_id] = handler
			print "Socket store is %s" % self.sockets
			
	def remove_socket(self, socket_id):
		del self.sockets[socket_id]
		
	def get_socket(self, socket_id):
		with self.__socket_lock:
			return self.sockets[socket_id]
		
	def open_socket(self, port):
		opened_socket = socketutil.server_socket(port)
		socket_id = "%s:%d" % opened_socket.getsockname()
		StageSocket(opened_socket, socket_id, self, self.__overlay.here).start()
		return socketutil.SocketReference(self.__overlay.here, socket_id)
	
	def connect_socket(self, address):
		socket = socketutil.client_socket()
		socket.connect(address)
		socket_id = "%s:%d" % socket.getsockname()
		log.debug(self,"Connected socket is %s %s" % (socket, socket.getsockname()[1]))
		StageSocket(socket, socket_id, self).start()
		return socketutil.SocketReference(self.__overlay.here, socket_id)

class StageSocket(threading.Thread):

	def __init__(self, socket, socket_id, store, manager_loc):
		threading.Thread.__init__(self)
		log.debug(self, "New socket at %s" % socket_id)
		self.__socket = socket
		self.__id = socket_id
		self.__store = store
		self.__store.add_socket(socket_id, self)
		self.__exit = False
		self.__manager_loc = manager_loc
		self.access = threading.Lock()
		self.control = threading.Lock()
		self.action = threading.Lock()
		self.result = threading.Lock()
		self.action.acquire()
		self.result.acquire()

	def run(self):
		while self.action.acquire(True):
			if self.__exit:
				break
			try:
				self.control.acquire()
				print "Do call %s on socket with %s and %s " % (self.method, self.args, self.kwds)
				method = getattr(self.__socket,self.method)
				self.__the_result = method(*self.args, **self.kwds)
				self.control.release()
				self.result.release()
			except Exception, e:
				log.debug(self, e)
				if(self.__exit):
					self.__the_result = "Socket closed"
					self.control.release()
					self.result.release()
					break
		
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		else:
			print "No attr %s for listening socket" % name
			if hasattr(self.__socket, name):
				print "But it's socket has %s" % name
				return SocketMethodCall(self, name, (self.access, self.action, self.control, self.result), self.__store, self.__manager_loc)
		
	def setCall(self, method, *args, **kwds):
		self.method = method
		self.args = args
		self.kwds = kwds
		
	def getResult(self):
		return self.__the_result
		
	def close(self):
		print "Closing socket %s" % self.__id
		self.__exit = True
		self.__socket.close()
		self.action.release()
		self.__store.remove_socket(self.__id)
		print "Closed %s" % self.__id 
	
class SocketMethodCall(object):
		
	def __init__(self, socket, method, locks, store, manager_loc):
		self.socket = socket
		self.method = method
		self.access, self.action, self.control, self.result = locks
		self.store = store
		self.manager_loc = manager_loc
		
	def __call__(self, *args, **kwds):
		print "Calling %s with %s and %s" % (self.method, args, kwds) 
		self.access.acquire()
		print "Got access"
		self.socket.setCall(self.method, *args, **kwds)
		self.action.release()
		self.result.acquire()
		self.control.acquire()
		res = self.socket.getResult()#getattr(self.__socket, self.method)(*self.args, **self.kwds)
		if self.method == 'accept':
			print "Accepted socket is %s %s" % res
			socket_id = "%s:%d" % res[1]
			StageSocket(res[0], "%s:%d" % res[1], self.store, self.manager_loc)
			return socketutil.SocketReference(self.manager_loc, socket_id)
		#print "Got %s:%d" % res
		self.control.release()
		self.access.release()
		return res