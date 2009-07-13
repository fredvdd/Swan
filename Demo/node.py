from Actors.keywords import *
from Actors.Common.theatre import RegisteredTheatre
from Demo.Pong.pongmanager import PongTheatres
  
# I start an empty theatre  
  
def start():
  RegisteredTheatre()
  
if __name__ == '__main__':
  initialise(start)