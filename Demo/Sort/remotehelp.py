from Actors.keywords import *
from Demo.Sort.sorter import Sorter

class Helper(MobileActor):

  def birth(self):
    a = Sorter()
    b = Sorter()
    pass
    
def start():
    Helper()        

if __name__ == '__main__':
  initialise(start)
