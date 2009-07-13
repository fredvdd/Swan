from Actors.keywords import *
from time import sleep

class Pinger(MobileActor):
  
  def birth(self):
    print('P: Started')
    moving = find_type('MigrateTest')
    print('P: Found moving, ' + moving.actor_id)

    for i in range(1,500):
      moving.ret(i, "This is a very very very very very very very long string")
 
      if i == 250:
        moving.start_migrate()
    #  print('P: '),
    #  print(reply),
     # print(' from ' + moving.actor_id)
     # sleep(0.05)

def start():
    Pinger()

if __name__ == '__main__':
  initialise(start)
