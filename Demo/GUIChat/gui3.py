from Actors.keywords import *
from Demo.GUIChat import chatwindow

def start():
  chatwindow.ConsoleUser('harry', 'green')
  
if __name__ == '__main__':
  initialise(start)