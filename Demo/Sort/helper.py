from Actors.keywords import *


class Helper(MobileActor):

  def birth(self):
    pass
    
def start():
    Helper()        

if __name__ == '__main__':
  initialise(start)
