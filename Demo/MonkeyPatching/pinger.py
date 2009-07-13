from Actors.keywords import *
from Demo.MonkeyPatching.shout import Shout
from Demo.MonkeyPatching.patcher import Patcher
from time import sleep

class Pinger(MobileActor):

  def birth(self):
    shout_outs = list()
    for i in range(0, 10):
      shout_outs.append(Shout())
      print shout_outs[i].actor_id
  
    patcher = Patcher()
    patcher.patch()
    for j in range(0, 10):
      sleep(1)
      for shout in shout_outs:
        print shout.say()
        
def start():
    Pinger()        
    
if __name__ == '__main__':
  initialise(start)
