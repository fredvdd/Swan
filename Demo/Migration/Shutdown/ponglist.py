from Actors.keywords import *
from Actors.Device.timer import *

TIME_STEP = 2

class PongList(NetworkSingletonActor):
  
  def birth(self):
    print 'PongList born'
    self.time = 0
    self.pongers = []
    AsyncTimer(my('tick'), TIME_STEP)
    
  def tick(self):
    for ponger in self.pongers:
      ponger.pong(self.time)
    self.time += TIME_STEP
  
  def add(self, actor):
    self.pongers.append(actor)
    
  def remove(self, actor):  
    if actor in self.pongers:
      self.pongers.remove(actor)
  
  def arrived(self):
    print 'PongList is here now!'
    Timer(my('tick'), TIME_STEP)
  
  def actorlost(self, actor, message):
    print 'Lost actor %s' % actor
    self.remove(actor)
  
  def theatreclosing(self):
    migrate_or_die()
