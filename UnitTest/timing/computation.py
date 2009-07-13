from Actors.keywords import *
import time
import math


class AWorker(MobileActor):
  
  def birth(self):
    pass
  
  def start(self):
    i = 0
    while i < 150000:
      self.is_prime(i)
      i += 1

  def is_prime(self, n):
      n = abs(n)
      i = 2
      while i <= math.sqrt(n):
          if n % i == 0:
              return False
          i += 1
      return True


class CompTest(MobileActor):

  def birth(self):
    begin = time.time()
    a = AWorker()
    b = AWorker()
    c = AWorker()
    d = AWorker()
    aa = a.start()
    bb = b.start()
    cc = c.start()
    dd = d.start()
    sync(aa)
    sync(bb)
    sync(cc)
    sync(dd)
    fin = time.time()
    print 'Time: ' + str(fin - begin)
    

def start():
  CompTest()

if __name__ == '__main__':
  initialise(start)


