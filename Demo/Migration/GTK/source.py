from Actors.keywords import *
import common

class Source(LocalActor):
  
  def birth(self):
    if sync(common.GUIList().addhost(here())):
      common.GUI()
    
def start():
  Source()
  
if __name__ == '__main__':
  initialise(start)
