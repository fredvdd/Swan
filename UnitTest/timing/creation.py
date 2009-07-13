from Actors.keywords import *
import time
import math

class Ping(MobileActor):
  
  def birth(self, to):
    self.to = to
    self.count = 0
  
  def start(self):
    i = 0
    while i < 30000:
      ret = self.to.inc()
      i += 1
      sync(ret)
      
  def inc(self):
    self.count += 1
    return self.count
      
class Pong(MobileActor):

  def birth(self):
    self.count = 0
  
  def start(self, to):
    self.to = to
    #self.send()

  def send(self):
    i = 0
    while i < 30000:
      ret = self.inc()
      sync(ret)
            
  def inc(self):
    self.count += 1
    return self.count



class CompTest(MobileActor):

  def birth(self):
    begin = time.time()
    i = 0
    while i < 2000:
      a = Pong()
      i += 1
 
    fin = time.time()
    print 'Time: ' + str(fin - begin)
    

def start():
  CompTest()


if __name__ == '__main__':
  initialise(start)


