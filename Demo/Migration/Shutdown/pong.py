from Actors.keywords import *
from ponglist import PongList

class Ponger(LocalActor):
  
  def birth(self):
    self.server = PongList()
    self.server.add(self)
      
  def pong(self, t):
    print 'Time %s' % t
    
  def theatreclosing(self):
    self.server.remove(self)

def start():
  Ponger()  

if __name__ == '__main__':
  initialise(start)