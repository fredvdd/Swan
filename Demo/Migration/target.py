from Actors.keywords import *

class Target(LocalSingletonActor):
  
  def birth(self):
    for i in range(0, 10):
      Foo()
  
  def imhere(self):
    print 'The badger has arrived'

class Foo(MobileActor):
  pass

def start():
  Target()
  
if __name__ == '__main__':
  initialise(start)