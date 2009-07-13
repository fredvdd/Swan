from Actors.keywords import *
import time

class Sleeper(LocalActor):
  
  def birth(self, seconds):
    self.seconds = seconds
    
  def sleep(self):
    time.sleep(self.seconds)
    return
    
class Timer(LocalActor):  
   
  def birth(self, target, seconds):
      self.target = target
      self.seconds = seconds
      self.joinactor('run', [True]) 
        
class AsyncTimer(Timer):
      
  def run(self, *args):
    time.sleep(self.seconds)
    self.target()
    self.joinactor('run', [])

class SyncTimer(Timer):
 
  def run(self, result):
    callback('run', self.target())
    time.sleep(self.seconds)

  def halt(self):
    die()

class WallClockTimer(LocalActor):
  
  def start(self):
    self.starttime = time.time()
    return self
    
  def stop(self):
    self.endtime = time.time()
    return self
  
  def elapsed_seconds(self):
    return self.endtime - self.starttime
  
class Clock(LocalActor):
  
  def time_in_seconds(self):
    return time.time()  