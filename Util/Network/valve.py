import socketutil
import threading
import cPickle as pickle
import socket
import traceback
from  Util.exceptions import AbstractMethodException

class Valve(threading.Thread):

  def __init__(self, port, log):
    threading.Thread.__init__(self)
    self.__port = port
    self.__exiting = False 
    self.__log = log

  def listen(self):
    self.__socket = socketutil.server_socket(self.__port)
    self.start()
  
  def incoming(self, object):
    raise AbstractMethodException()
  
  def run(self):
    while True:
      try:
        (clientsocket, s) = self.__socket.accept()
        Worker(clientsocket, self, self.__log).start()
      except:
       if self.__exiting:
         return
        
  def shutdown(self):
    self.__log.debug(self, 'shutting down')
    self.__exiting = True
    try: 
      self.__socket.close()
    except Exception, e:
      print 'ERROR;', e.args

      
class Worker(threading.Thread):

  def __init__(self, socket, valve, log):
    threading.Thread.__init__(self)
    self.__socket = socket
    self.__valve = valve
    self.__log = log
    
  def run(self):
      while(True):
        #print self.__socket.getsockname()
        #print self.__socket.getpeername()
        obj = pickle.load(self.__socket.makefile('r'))
        try:
          result = self.__valve.incoming(obj)
        except Exception, e:
          self.__log.error(self, traceback.format_exc())
          result = e
        pickle.dump(result, self.__socket.makefile('w'))
        self.__socket.close()
        return
