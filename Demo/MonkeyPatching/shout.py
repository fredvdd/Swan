from Actors.keywords import *

class Shout(MobileActor):
  
  def birth(self):
    self.message = 'Hello'
    
  def say(self):
    return self.message
      