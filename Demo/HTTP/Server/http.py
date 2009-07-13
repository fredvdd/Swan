from Actors.keywords import *
from Actors.Device.misc import RandomGenerator
from Actors.Common.theatre import TheatreList
from Demo.HTTP.session import Session
from Demo.HTTP.probe import Probe
from Demo.HTTP.naming import NameServer
from Util.exceptions import AbstractMethodException

NUM_SLAVES = 10

class WebServer(MobileActor):
  """Abstract class representing a webserver"""
  
  def birth(self):
    self.createslaves()
    NameServer().register(self, self.hostname())

  def hostname(self):
    raise AbstractMethodException()
  
  def createslave(self):
    raise AbstractMethodException()

  def createslaves(self):
    self.slaves = []
    for i in range(0, NUM_SLAVES):
      self.slaves.append(self.createslave())
  
  def get(self, source, session, page):
    """The main entry point to the webserver"""
    if session == None:
      session = Session()
    return self.randomslave().get(source, session, page)
  
  def randomslave(self):
    """Internal utility method for randomly secting a slave"""
    index = sync(RandomGenerator().getrandom(0, len(self.slaves) -1))
    return self.slaves[index]
  
class WebServerSlave(MobileActor):
  
  def get(self, source, session, page):
    raise AbstractMethodException()
