from Actors.keywords import *

class MessageSend(MobileActor):
  
  def birth(self):
    print('started')
    sim = find_type('Simple')
    print('attempting msg ' + sim.actor_id)
    print(str(sim.add()))
    print('msg sent')
  
def start():
  MessageSend()

if __name__ == '__main__':
  initialise(start)

