from Actors.keywords import *
import math

def f(x):
  return (math.sin(x**3.0-1.0)/(x+1))*math.sqrt(1.0+math.exp(math.sqrt(2.0*x)))
    
def xi(i, h):
  return (i-1) * h

class TrapWorker(StaticActor):
  
  def birth(self):
    pass
    
  def arrived(self):
    self.approximate()
  
  def approximate(self, h, lower, upper):
    print 'worker has msg'
    diff = (upper - lower) / float(h)
    result = 0.0
    for i in range(0, h):
       start = lower + diff * i
       fin = start + diff
       result += ((f(start) + f(fin)) * (diff / 2))
    return result
    
  def kill(self):
    die()