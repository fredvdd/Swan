from Actors.keywords import *
import time
    
# The mouse event interface has been disabled due
# to its poor performance on slow computers.

class Mouse(LocalActor):

  def birth(self, actor):
    self.actor = actor
    self.mouse_at = (0, 0)
    # Begin polling the mouse's position
    # schedule('tell')

  def mousemove(self, x, y):
    # We only need to store the last position
    # of the mouse, the history of the mouse's
    # position is of little use
    self.mouse_at = (x, y)
      
  def tell(self):
    # This method polls the mouse's position
    (x, y) = self.mouse_at
    self.actor.mousemove(x, y)
    schedule('tell')
    time.sleep(0.1)
    
  def kill(self):
    die()