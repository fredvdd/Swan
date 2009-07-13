from Actors.keywords import *
from badger import *

class Source(LocalActor):
  
  def birth(self):
    badger = Badger()
    sync(badger.cough())
    sync(badger.chase())
    badger.cough()
    print sync(badger.getname())
    
def start():
  Source()  

if __name__ == '__main__':
  initialise(start)
