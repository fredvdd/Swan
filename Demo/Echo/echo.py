from Actors.keywords import *
from Demo.Echo.server import EchoServer

class EchoClient(MobileActor):
  
  def birth(self):
    self.generate_messages()
      
  def generate_message(self):
    print EchoServer().echo('test message')
   
def start():
  EchoClient()

if __name__ == '__main__':
  initialise(start)