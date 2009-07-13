from Actors.keywords import *
from Actors.Common.server import GenericServer

class EchoServer(GenericServer):
  
  def birth(self):
    print 'Echo server born'

  def echo(self, message):
    return "echo:> " + message

def start():
    Echo()
    
if __name__ == '__main__':
  initialise(start)
