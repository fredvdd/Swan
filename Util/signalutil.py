import threading, time, os, sys, operator, traceback
from Util import exceptions

class NewRunner(object):
      
  def start(self):
  #  signal.signal(signal.SIGINT, self.shutdown_sig)
  #  signal.signal(signal.SIGTERM, self.shutdown_sig)
    try:
      self.begin()
    except Exception, e:
      trace = traceback.format_exc()
      try:
        self.shutdown()
      except Exception:
        print 'Warning unsafe shutdown'
      print e
      print trace
      return
    signal.pause()
          
  def shutdown_sig(self, *args):
    self.shutdown()

  def begin(self):
    raise exceptions.AbstractMethodException()

  def shutdown(self):
    raise exceptions.AbstractMethodException()

  
class Runner(object):

  def start(self):
    try:
      import signal
      signal.signal(signal.SIGINT, self.shutdown_sig)
      signal.signal(signal.SIGTERM, self.shutdown_sig)
    except ImportError:
      pass
    try:
      self.begin()
    except Exception, e:
      trace = traceback.format_exc()
      try:
        self.shutdown()
      except Exception:
        print 'Warning unsafe shutdown'
      print e
      print trace
      return
    signal.pause()

  def shutdown_sig(self, *args):
    self.shutdown()

  def begin(self):
    raise exceptions.AbstractMethodException()

  def shutdown(self):
    raise exceptions.AbstractMethodException()

