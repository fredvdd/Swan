import time
import Util.ids as ids
from Queue import Queue
import sys

class Terminal(object):
  
  def __init__(self, theatre, loc):
    self.theatre = theatre
    self.queue = Queue()
    self.loc = loc
    try:
      import signal
      signal.signal(signal.SIGINT, self.signal_handler)
      signal.signal(signal.SIGTERM, self.signal_handler)
    except: 
      pass

  def shell(self):
    self.execute = True
    while self.execute:
      time.sleep(5)
    while False:
      print (self.loc + '>'),
      try:
        command = sys.stdin.readline().strip()
      except:
        execute == False
        command = 'exit'
      if command == 'exit':
        execute = False
      else:
        if command.startswith('import '):
          # TODO: import
          pass
        else: 
          try:
            exec(command)
          except:
            print 'command not found'
    self.theatre.shutdown()
  
  def signal_handler(self, signal, frame):
    self.execute = False
    
  def says(self):
    print("")
    while not self.queue.empty():
      (id, msg) = self.queue.get()
      print(ids.type(id) + " (from" + ids.port(id) + ") says: " + msg)
      if self.queue.empty():
        timing.sleep(1)
      print(self.loc + '>')
