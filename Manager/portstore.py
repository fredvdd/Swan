import threading
from Util.Network import socketutil
from Manager.managerlog import log

class PortStore(object):
	def __init__(self):
		self.__port_lock = threading.Lock()
		self.__client_lock = threading.Lock()
		self.listening_ports = {}
		self.client_ports = {}
	
	def add_port(self, port, handler):
		self.__port_lock.acquire()
		self.listening_ports[port] = handler
		self.__port_lock.release()
		
	def add_client_port(self, port, handler):
		self.__client_lock.acquire()
		self.client_ports[port] = handler
		self.__client_lock.release()
		
	def open_port(self, port):
		ListeningPort(port, self).start()
		
	def close_port(self, port):
		self.listening_ports[port].shutdown()
		
	def accept(self, port):
		return self.listening_ports[port].accept()
		
	def read(self, port, size):
		return self.client_ports[port].read(size)
		
	def write(self, port, string):
		return self.client_ports[port].write(string)

class ListeningPort(threading.Thread):

	def __init__(self, port, parent):
		threading.Thread.__init__(self)
		parent.add_port(port, self)
		self.semaphore = threading.Semaphore(1)
		self.accepting = threading.Lock()
		self.__port = port
		self.__exiting = False
		self.accept_lock = threading.Lock()
		self.accept_lock.acquire()

	def run(self):
		self.__socket = socketutil.server_socket(self.__port)
		print "Port %d bound and waiting" % self.__port
		while self.semaphore.acquire(True):
			try:
				print "Accepting on port %d" % self.__port
				(clientsocket, address) = self.__socket.accept()
				ClientPort(clientsocket, address, self).start()
				self.accepted = "%s:%d" % clientsocket.getpeername()
				self.accept_lock.release()
				print "Accepted from %s" % self.accepted
			except Exception, e:
				log.debug(self, e)
				if self.__exiting:
					return

	def accept(self):
		with self.accepting:
			self.accept_lock.acquire()
			ret = self.accepted
			self.semaphore.release()
		return ret
	
	def shutdown(self):
		#self.__log.debug(self, 'shutting down')
		self.__exiting = True
		try: 
			self.__socket.close()
			self.semaphore.release()
		except Exception, e:
			print 'ERROR;', e.args

class ClientPort(threading.Thread):

	def __init__(self, socket, address, parent):
		threading.Thread.__init__(self)
		#parent.add_client_port("%s:%d" % socket.getpeername(), self)
		self.socket = socket
		self.address = address
		self.rfile = socket.makefile('r')
		self.wfile = socket.makefile('w')
		self.access_lock = threading.Lock()
		self.action = threading.Lock()
		self.read_lock = threading.Lock()
		self.write_lock = threading.Lock()
		
	def run(self):
		print "Handling %s, %d" % self.address
		self.action.acquire()
		self.read_lock.acquire()
		self.read_done.acquire()
		self.write_lock.acquire()
		
		while self.action.acquire():
			if self.read_lock.acquire(False):
				self.read_str = self.socket.read(self.size)
				self.read_done.release()
			if self.write_lock.acquire(False):
				pass


	def read(self, size):
		with self.access_lock:
			self.size = size
			self.read_lock.release()
			self.write_lock.acquire()
			self.action.release()
			with self.read_done:
				return self.read_str
