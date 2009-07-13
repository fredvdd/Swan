from Actors.keywords import *
from Demo.TrapAproxPool.worker import TrapWorker
import time

class TrapCoordinator(MobileActor):
  
  def birth(self, samples, lower, upper):
    
    start = time.time()
    
    samples_per_msg = int(samples / (upper - lower))
    
    lowers = range(lower, upper - 1)
    uppers = range(lower + 1, upper)
    samples = [samples_per_msg for x in lowers]
        
    worker_pool = get_pool(TrapWorker)
      
    results = worker_pool.approximate(samples, lowers, uppers) 
    result = sum(results)

    total = time.time() - start
   
    print "%s&%s" % (result, total)

