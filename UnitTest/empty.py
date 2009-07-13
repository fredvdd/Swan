from Actors.keywords import *

class Empty(MobileActor):
  
  def birth(self):
    self.empty = ""
      

def start():
    Empty()

if __name__ == '__main__':
  initialise(start)