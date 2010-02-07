import threading
from Util.Network import socketutil, rpc
from Manager.managerlog import log
from Messaging.structures import MessageQueue, ResultMap

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
		log.debug(self, "Opened socket %d" % port)
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

	def __init__(self, sock, socket_id, store, manager_loc):
		threading.Thread.__init__(self)
		log.debug(self, "New socket at %s" % socket_id)
		self.sock = sock
		self.wfile = sock.makefile('w')
		self.rfile = sock.makefile('r')
		self.id = socket_id
		self.store = store
		self.store.add_socket(socket_id, self)
		self.exit = False
		self.manager_loc = manager_loc
		self.messages = MessageQueue()
		self.results = ResultMap()
		self.m_id = 0

	def run(self):
		while not self.exit:
			try:
				request = self.messages.get_next()
				if self.exit:
					break
				mid, target, method, args, kwds = request
				print "Call %s on %s with %s and %s" % (method, target, args, kwds)
				meth = getattr(target, method)
				result = meth(*args, **kwds)	
				#special cases
				if method == 'makefile':
					#print "Called makefile %s, %s, %s" % (self.manager_loc, self.id, args[0][0])
					result = socketutil.SocketFileReference(self.manager_loc, self.id, args[0][0])
				elif method == 'accept':
					socket_id = "%s:%d" % result[1]
					StageSocket(result[0], socket_id, self.store, self.manager_loc).start()
					result = socketutil.SocketReference(self.manager_loc, socket_id)
				self.results.add(SocketResult(mid,result))
			except Exception, e:
				log.debug(self, e)
				if self.exit:
					break
		#print "Socket %s run out" % self.id
		
	def __getattr__(self, name):
		if self.__dict__.has_key(name):
			return self.__dict__[name]
		elif name.find(':') > 0:
			#print "No attr %s for listening socket" % name
			targetname, method = name.split(':')
			target = getattr(self, targetname)
			if hasattr(target, method):
				#print "But it's socket has %s" % name
				self.m_id = self.m_id + 1
				return SocketRequest(self, self.m_id, target, method)
		
	def close(self):
		print "Closing socket %s" % self.id
		self.exit = True
		self.messages.add(None)
		self.sock.close()
		self.store.remove_socket(self.id)
		log.debug(self, "Closed socket %s" % self.id) 
	
class SocketRequest(object):
		
	def __init__(self, socket, mid, target, method):
		self.socket = socket
		self.mid = mid
		self.target = target
		self.method = method
		
	def __call__(self, *args, **kwds):
		#print "Calling %s with %s and %s" % (self.method, args, kwds)
		self.socket.messages.add((self.mid, self.target, self.method, args, kwds))
		#print "Request made"
		return self.socket.results.wait_for(self.mid).result
		
class SocketResult(object):
	
	def __init__(self, mid, result):
		self.id = mid
		self.result = result