from Actors.keywords import *

class Marker(LocalActor):
  
  def mark(self, answer):
    return answer == 'Cat'  
  
class Lecturer(LocalActor):
  
  def birth(self):
    m1 = Marker()  
    m2 = Marker()
    
    print sync(m1.mark('Cat'))
    print sync(m2.mark('Dog'))

def start():
  Lecturer()

if __name__ == '__main__':  
  theatre.initialise(start)