from Actors.keywords import *
import os

class TheatreStatus(LocalSingletonActor):
  
  def loadaverage(self):
    return os.getloadavg()

  def osname(self):
    return os.name
  
  def uptime(self):
    return os.popen('uptime').read()