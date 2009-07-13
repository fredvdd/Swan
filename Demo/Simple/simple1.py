from Actors.keywords import *

class Marker(Actor):
  
  def mark(self, answer):
    return answer == 'Cat'  
  
class Lecturer(Actor):
  
  def birth(self):
    m1 = Marker()  
    m2 = Marker()
    
    print sync(
      m1.mark('Cat'), 
      m2.mark('Dog')
    )
    
def start():
  Lecturer()
  
if __name__ == '__main__':
  initialise(start)
  
