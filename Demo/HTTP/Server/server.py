from Actors.keywords import *
from Demo.HTTP.Server.Sites.monitor import MonitorWebServer
from Demo.HTTP.Server.Sites.ndunn import NDunnWebServer

def start():
  MonitorWebServer()
  NDunnWebServer()
  
if __name__ == '__main__':
  initialise(start)