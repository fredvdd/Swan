from Actors.keywords import *
from Demo.LoadBal.worker import Worker
from Actors.Common.Balance.balancer import LoadBalancer
from Actors.Common.Balance.probing import ProbingStrategy
from Actors.Common.theatre import TheatreList
from Actors.Device.misc import RandomGenerator
import time

class LoadGenerator(LocalActor):
  
  def birth(self):
    TheatreList().addchild(here())
  
    LoadBalancer().set_strategy(ProbingStrategy())
    gen = RandomGenerator()

    for i in range(0, 200):
      time.sleep(0.2)
      sleepyness = sync(gen.getrandom(2, 6))
      Worker(sleepyness / 1000.0)

def start():
  LoadGenerator()
  
  
    
if __name__ == '__main__':
  initialise(start)