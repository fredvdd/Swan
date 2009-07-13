from Actors.keywords import *
import math

def f(x):
  return (math.sin(x**3.0-1.0)/(x+1))*math.sqrt(1.0+math.exp(math.sqrt(2.0*x)))
    
def xi(i, h):
  return (i-1) * h

class TrapWorker(MobileActor):
  
  def birth(self, theatre, a, h, lower, upper):
    self.upper = upper
    self.lower = lower
    self.h = h
    migrate_to(theatre)
    
  def arrived(self):
    self.approximate()
  
  def approximate(self):
    h = self.h
    result = 0.0
    for i in range(self.lower, self.upper):
       result += (f(xi(i, h)) + f(xi(i+1, h))) * (h / 2)
    self.partial_result = result
    
  def result(self):
    return self.partial_result
  
  def kill(self):
    die()