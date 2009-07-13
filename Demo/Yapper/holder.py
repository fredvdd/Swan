from Actors.keywords import *

class Holder(MobileActor):
  def birth(self):
    pass
    
def start():
  Holder()

if __name__ == '__main__':
  initialise(start)