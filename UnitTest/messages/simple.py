from Actors.keywords import *

class Simple(MobileActor):
  
  def birth(self):
    self.num = 1
    print("created")
  
  def add(self):
    self.num += 1
    print("add has run")
    return self.num

      
def start():
  Simple()

if __name__ == '__main__':
  initialise(start)

