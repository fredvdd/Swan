from Actors.keywords import *

class Session(MobileActor):
  
  def birth(self):
    self.data = dict()
  
  def put(self, key, value):
    self.data[key] = value 
  
  def get(self, key):
    if key in self.data:
      return self.data[key]
    return None 

  def destroy(self):
    die()