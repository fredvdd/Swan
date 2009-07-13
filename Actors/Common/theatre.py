from Actors.keywords import * 
from server import BServer

class TheatreList(BServer):
  
  def birth(self):
    BServer.birth(self)
    self.listeners = []
  
  def theatres(self):
    return self.children
  
  def changed(self):
    for listener in self.listeners:
      listener()
  
  def register(self, target):
    self.listeners.append(target)

class RegisteredTheatre(LocalActor):
  
  def birth(self):
    TheatreList().addchild(here())
    
  def theatreclosing(self):
    TheatreList().removechild(here())