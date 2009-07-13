from Actors.keywords import *
  
class Badger(MobileActor):
  
  def birth(self):
    self.name = "Mr Badger"
    
  def arrived(self):
    local('Target').imhere()
    
  def chase(self):
    migrate_to('mrbadger:8000')
    
  def cough(self):
    print "Cough cough"  
    
  def getname(self):
    return self.name