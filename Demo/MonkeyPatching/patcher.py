from Actors.keywords import *
from time import sleep

class Patcher(MobileActor):

  def birth(self):
    pass
  
  def patch(self):
    sleep(2)
    shouts = find_all_types('Shout')
    for shout in shouts:
      print 'shout updating', shout.actor_id
      update_method(shout, say)

def say(self):
  return (self.message.upper() + '!!!')
