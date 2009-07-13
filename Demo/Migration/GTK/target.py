from Actors.keywords import *
import common

class Target(LocalSingletonActor):
  
  def imhere(self):
    print 'The badger has arrived'

def start():
  Target()
  
if __name__ == '__main__':
  initialise(5145, socket.gethostname(), 7000, start)






