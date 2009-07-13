import threading
from Util import exceptions

class Logger(object):
  
  def debug(self, obj, message):
    self.write_debug("DEBUG [%s] %s" % (obj, message))
  
  def exception(self, exception):
    self.write_debug("EXCEPTION %s" % exception)
  
  def warn(self, obj, message):
    self.write_warn("WARN [%s] %s" % (obj, message))
    
  def error(self, obj, message):
    self.write_error("ERROR [%s] %s" % (obj, message))  
    
  def write_warn(self, string):
    raise exceptions.AbstractMethodException()

  def write_error(self, string):
    raise exceptions.AbstractMethodException()  
    
  def write_debug(self, string):
    raise exceptions.AbstractMethodException()

  def write_exception(self, string):
    raise exceptions.AbstractMethodException()
  
  
class TerminalLogger(Logger):
 
  def write_debug(self, string):
    print string

  def write_exception(self, string):
    print string

  def write_warn(self, string):
    print string

  def write_error(self, string):
    print string 

class FileLogger(Logger):
  
  def __init__(self, filename):
    self.__log_lock = threading.Lock()
    self.__log_file = open(filename, 'a')
    self.__log_file.flush()

  def write_debug(self, string):
    self.__write_to_file(string)
    
  def write_exception(self, string):
    self.__write_to_file(string)
  
  def write_warn(self, string):
     self.__write_to_file(string)

  def write_error(self, string):
     self.__write_to_file(string)
  
  def __write_to_file(self, string):
    self.__log_lock.acquire()
    self.__log_file.write(string + '\n')
    self.__log_file.flush()
    self.__log_lock.release()
    
class NullLogger(Logger):
  
  def write_debug(self, string):
    pass
    
  def write_exception(self, string):
    pass
  
  def write_warn(self, string):
    pass

  def write_error(self, string):
    pass
    


