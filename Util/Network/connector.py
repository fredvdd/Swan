import socketutil
import cPickle as pickle
import sys

class Connector(object):
  def __init__(self, fulladdress):
   (self.__address, strport) = fulladdress.split(':')
   self.__port = int(strport)
    
  def connect(self):
    self.__socket = socketutil.client_socket()
    self.__socket.connect((self.__address, self.__port) )
            
  def send(self, obj):
    if sys.platform == 'symbian_s60':
      self.__socket.send(pickle.dumps(obj,0))
    else:
      pickle.dump(obj, self.__socket.makefile('w'))
    
   
  def receive(self):
    if sys.platform == 'symbian_s60':
      # TODO: loopify to deal with > 4096
      return pickle.loads(self.__socket.recv(4096))
    else:
      return pickle.load(self.__socket.makefile('r'))
    
    
    
  def disconnect(self):
    #self.send('CLOSE')
    self.__socket.close()
