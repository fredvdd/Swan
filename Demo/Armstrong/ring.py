from Actors.keywords import *
from Actors.Device.timer import WallClockTimer
import sys

MESSAGE_PASSES = 100000

class StartNode(MobileActor):

  def birth(self, n, loops):
    self.n = n
    self.max_loops = loops
    self.loops = 0
    
    self.clock = WallClockTimer().start()
    next = self
    for i in range(0, n):
      next = RingNode(next)  
    self.next = next
    next.accept()
  
  def accept(self):
    self.loops += 1
    if self.loops == self.max_loops:
      self.clock.stop()
      elapsed = self.clock.elapsed_seconds()
      print "%s\t\t&%s" % (self.n, elapsed / (self.n*self.max_loops))
    else:
      self.next.accept()

class RingNode(MobileActor):
  
  def birth(self, next):
    self.next = next
  
  def accept(self):
    self.next.accept()
  
def start():
  actors = int(sys.argv[1])
  loops = MESSAGE_PASSES / actors
  print "Using %d loops" % loops
  if MESSAGE_PASSES % actors != 0:
    print 'ERROR'
  StartNode(actors, loops)

if __name__ == '__main__':
  initialise(start)