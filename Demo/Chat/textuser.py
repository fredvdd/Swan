from Actors.keywords import *
from Actors.Device.input import Keyboard
from Demo.Chat.server import ChatServer

class User(MobileActor):
  
  def birth(self):
    self.server = ChatServer()
    self.server.addchild(self.incoming)
    Keyboard().listen(self.typed)
      
  def typed(self, msg):
    self.server.say(msg) 
      
  def incoming(self, msg):
    print ">" + msg

def start():
    User()

if __name__ == '__main__':
  initialise(start)

