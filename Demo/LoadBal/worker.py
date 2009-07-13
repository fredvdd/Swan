from Actors.keywords import *
from Actors.Common.Balance.balancer import BalancedActor
import time

class Worker(BalancedActor):
  
  def birth(self, sleeptime):
    BalancedActor.birth(self)
    self.sleeptime = sleeptime
    self.count = 0
    schedule('work')
  
  def arrived(self):
    BalancedActor.arrived(self)
    schedule('work')

  def work(self):
    self.count += 1
    time.sleep(self.sleeptime)
    schedule('work')