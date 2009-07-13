from Actors.keywords import *
from ponggui import PongWindow
from pongmanager import PongTheatres, PongPlayers

class Player(MobileActor):
  
  def birth(self):
    self.window = PongWindow(self)
    PongPlayers().add(self)
    self.score = 0
    self.availabletheatres(PongTheatres().get())
  
  def availabletheatres(self, theatres):
    self.window.settheatres(theatres, self.score)
  
  def getbatpc(self):
    return (self, self.window.getbatpc())
  
  def incoming(self, ball):
    self.window.incoming(ball)
    
  def leaving(self, ball, hit):
    if hit:
      self.score += 1
    else:
      self.score -= 1
     # self.availabletheatres(PongTheatres().get())
    PongPlayers().leaving()
    
  def migraterequested(self, theatre):
    migrate_to(theatre)
    
  def theatreclosing(self):
    sync(PongPlayers().remove(self))
    
  def arrived(self):
    self.window.migrate_to(here())
    self.availabletheatres(PongTheatres().get())