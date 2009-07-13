from Actors.keywords import *
from moving import MigrateTest

class Source(MobileActor):
  
  def birth(self):
    mgrt_test = MigrateTest()

def start():
    Source()

if __name__ == '__main__':
  initialise(start)
