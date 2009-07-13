from Actors.keywords import *
from Actors.Device.GTK.drawing import *
from Actors.Device.timer import SyncTimer
import time
import threading

BALL_SIZE = 20

class Ball(MobileActor):
   
  def birth(self):
    self.speed = 14
    self.xdir = 0.7
    self.ydir = 1
    self.x = 0
    self.y = 100
    self.stopped = True
    self.rect = None
    self.parked = True
    self.bounds = None
  
  def attach(self, window, theatre, bounds):
    """Attach this ball to a canvas"""
    self.window = window
    self.bounds = bounds
    self.rect = sync(self.window.addball(self.x, self.y, BALL_SIZE, BALL_SIZE))
    self.migrate_to(theatre)
    
  def getpc(self):
    """Return the ball's position as a percentage, 
       used by the picture in picture API"""
    if not self.bounds:
      return (0.0, 0.0)
    return (float(self.x) / self.bounds[0], float(self.y) /self.bounds[1])
    
  def migrate_to(self, theatre):
    self.parked = False
    migrate_to(theatre)
    
  def park_at(self, theatre):
    self.parked = True
    migrate_to(theatre)
    
  def arrived(self):
    if not self.parked:
      self.unpause()
    
  def unpause(self):
    self.stopped = False
    schedule('tick')
    
  def pause(self):
    self.stopped = True  
  
  def theatreclosing(self):
    migrate_or_die()
    
  def hit(self):
    self.xdir = -abs(self.xdir)
    
  def tick(self):
    if self.stopped:
      # Stopped so ignore the ticks
      return 
    if self.y <= 0 and self.ydir < 0 or self.y >= self.bounds[1] - BALL_SIZE and self.ydir > 0:
      self.ydir = -self.ydir
    if self.x < 0 and self.xdir < 0 or self.x > self.bounds[0] and self.xdir > 0:
      self.rect.delete()
      won = self.x < 0
      self.x = 0
      self.xdir = abs(self.xdir)
      self.window.leaving(self, won)
      self.stopped = True
      return
    self.x += int(self.xdir * self.speed)
    self.y += int(self.ydir * self.speed)
    self.rect.setpos(self.x, self.y + 21)
    time.sleep(0.1)
    schedule('tick')