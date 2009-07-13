from Actors.keywords import *

class Dest(MobileActor):
  
  def birth(self):
    pass

def start():
    Dest()

if __name__ == '__main__':
  initialise(start)
