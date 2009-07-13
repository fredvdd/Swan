from Actors.keywords import *

class Simple(NetworkSingletonActor):
  
  def birth(self):
    print("SING, In singleton constructor")
    self.num = 0

  
  def inc(self):
    self.num += 1

  def get(self):
    print 'SING, get: ' +  str(self.num)
    return self.num


