from Actors.keywords import *
from UnitTest import simpleactors

class NamingTest(MobileActor):
  
  def birth(self):
    print("Naming as 'one'")
    name('one')

    print("Naming as 'two'")
    name('two')
    
    actor1 = find_name('one')
    if self.actor_id == actor1.actor_id:
      print("find of 'one' worked")

    actor2 = find_name('two')
    if self.actor_id == actor2.actor_id:
      print("find of 'two' worked")
    
    actor3 = find_type('NamingTest')
    if self.actor_id == actor3.actor_id:
      print("find of an actor of type 'NamingTest' worked")
    
    actor4 = simpleactors.SimpleSingleton("ss1")
    print (actor4.hi())

    actor5 = simpleactors.SimpleSingleton("ss1")
    print (actor5.hi())
  
    print(actor4)
    print (actor5)
    if (actor4 == actor5):
      print("actors are the same, singlton lookup worked")

    actor6 = simpleactors.SimpleSingleton("ss2")
    print (actor6.hi())

    if not (actor4 == actor6):
      print("actors are different, singlton lookup worked")
    
def start():
    NamingTest()

if __name__ == '__main__':
  initialise(start)


