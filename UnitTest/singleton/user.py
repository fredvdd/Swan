from Actors.keywords import *
from simplesingle import Simple

class MessageSend(MobileActor):
  
  def birth(self):
    sim = Simple()
    print('TEST, started')
    a = sim.get()
    print('TEST, a is: ' + str(a))
    a = sim.inc()
    a = sim.get()
    print('TEST, a is: ' + str(a))

  
def start():
  MessageSend()

if __name__ == '__main__':
  initialise(start)

