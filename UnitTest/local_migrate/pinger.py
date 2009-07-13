from Actors.keywords import *
from time import sleep
from moving import MigrateTest

class Pinger(MobileActor):
  
  def birth(self):
    print('P: Started')
    moving = MigrateTest()
    print('P: found Moving: ' + moving.actor_id)

    for i in range(1,100):
      moving.ret(i, "This is a very very very very very very very long string")
 
      if i == 50:
        moving.start_migrate()
      
    #  print('P: '),
    #  print(reply),
     # print(' from ' + moving.actor_id)
     # sleep(0.05)
     
  def pong(self, src):
    print("P: Pong from: " + src)

def start():
    Pinger()

if __name__ == '__main__':
  initialise(start)
