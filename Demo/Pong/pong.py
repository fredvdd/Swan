from Actors.keywords import *
from player import Player
from pongmanager import PongTheatres

class Pong(LocalActor):
  
  def birth(self):
    PongTheatres().add(here())
    Player()
    
  def theatreclosing(self):
    PongTheatres().remove(here())

def start():
   Pong()
   
if __name__ == '__main__':
  initialise(start)