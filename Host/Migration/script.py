import sys
import imp
import tempfile
import os
import threading

# TODO: Delete file

class ScriptManager(object):
  
  def __init__(self, theatre):
    self.__theatre = theatre
    self.__lock = threading.Lock()
  
  def add_script(self, modulename, modulesrc):
    self.__lock.acquire()
    name = '/tmp/%s-mobile-%s' % (self.__theatre, modulename)
    tmpfile = open(name, 'w')
    tmpfile.write(modulesrc)
    tmpfile.flush()  
    tmpfile.close()
    imp.acquire_lock()
    imp.load_source(modulename, name)
    imp.release_lock()
    tmpfile.close()
    self.__lock.release()
    
  def has_script(self, modulename):
    self.__lock.acquire()
    if sys.modules.has_key(modulename):
      self.__lock.release()
      return True
    try:
      __import__(modulename)
      self.__lock.release()
      return True
    except:
      self.__lock.release()
      return False