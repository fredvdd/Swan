from Actors.keywords import *
import sys

class Keyboard(MobileActor):
    
  def birth(self):
    self.listener = None
    
  def readline(self, target):
    try:
      line = sys.stdin.readline().strip()
      target.userwrote(line)
    except Exception:
       pass
    
  def do_read(self):
   line = sys.stdin.readline().strip()
   if self.listener:
     self.listener(line)
   schedule('do_read') 
     
  def listen(self, callback):
    self.listener = callback
    schedule('do_read') 
