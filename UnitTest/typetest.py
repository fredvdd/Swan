from Actors.keywords import *
from UnitTest import empty

class TypeTest(MobileActor):
  
  def birth(self):
    anEmptyActor = empty.Empty()
    anotherEmptyActor = empty.Empty()

    find()
    
    anEmptyActor.actor_id 
    
    
    actor1 = find('one')
    if self.actor_id == actor1.actor_id:
      print("find of 'one' worked")

    actor2 = find('two')
    if self.actor_id == actor2.actor_id:
      print("find of 'two' worked")
      
def start():
  TypeTest()

if __name__ == '__main__':
  initialise(start)

