from Actors.keywords import *

class Marker(Actor):
  
  def mark(self, answer):
    return answer == 'Cat'  
  
class Lecturer(Actor):
  
  def birth(self):
    m1 = Marker()  
    m2 = Marker()
    
    r1 = m1.mark('Cat')
    r2 = m2.mark('Dog')
    
    if not ready(r1):
      print 'Result one is not ready'
    
    print sync(r1)
    
    callback('marked', r2)
  
  def marked(self, result):
    print 'Called back'
    print result
    
    
def start():
  Lecturer()
  
if __name__ == '__main__':
  initialise(start)