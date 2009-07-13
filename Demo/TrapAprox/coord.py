from Actors.keywords import *
from Demo.TrapAprox.worker import TrapWorker
from Actors.Common.theatre import TheatreList
from Actors.Device.timer import WallClockTimer

class TrapCoordinator(MobileActor):
  
  def birth(self, n, actors, lower, upper):

    theatres = TheatreList().theatres()
    
    timer = WallClockTimer().start()
    
    h = (upper - lower) / float(n)
    work_per_actor = n / actors
    
    workers = []
    for i in range(0, actors):
      theatre = theatres[i % len(theatres)]
      start =  (work_per_actor * i) + 1
      end = start + work_per_actor
      workers.append(TrapWorker(theatre, lower, h, start, end))
    
    result = sum([worker.result() for worker in workers])
    
    timer.stop()
   
    print "%s&%s&%s\\\\" % (n,result, timer.elapsed_seconds())
    
    [worker.kill() for worker in workers]
    
    die()
