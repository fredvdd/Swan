from Actors.keywords import *

class RootSupervisor(MobileActor):
  
  def child_errored(self, child, error):
    pass

  def child_died(self, child):
    pass
  
  def child_migrated(self, child, to):
    pass
  
  def theatreclosing(self):
    migrate_or_die()

class Supervisor(RootSupervisor):
  
  def theatreclosing(self):
    migrate_or_die()
    
  def birth(self, parent):
    RootSupervisor.birth(self)
    self.parent = parent

  def start(self):
    pass

  def restart(self):
    pass

  def error(self, e):
    self.parent.child_errored(self, e)

  def arrived(self):
    self.parent.child_migrated(self, here())

  def kill(self):
    self.parent.child_died(self)
    die()


class Worker(MobileActor):

  def birth(self, parent):
    self.parent = parent

  def start(self):
    pass

  def restart(self):
    pass

  def error(self, e):
    self.parent.child_errored(self, e)

  def kill(self):
    callback('done', self.parent.child_died(self))
    die()
  
  def done(self):
    die()
  
class FixedWorker(Worker):
  """I am a worker which dies when my current theatre
     closes."""
  
  def theatreclosing(self):
    self.kill()
     
class MobileWorker(Worker):
  """I am a worker which migrates when my current theatre
      closes."""
          
  def theatreclosing(self):
    migrate_or_die()
    
  def arrived(self):
    self.parent.child_migrated(self, here())