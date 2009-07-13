from Actors.Device.GTK.widgets import *
from Actors.Device.GTK.layout import *
from Util.exceptions import AbstractMethodException

class SupervisionGUI(Window):
  
  def birth(self, target):
    self.target = target
    self.trace = Label("%s\n" % self.getname())
    options = HList(self.getoptions())
    Window.birth(self, VPair(self.trace, options))
    if self.mobile():
      self.keepalive()
    
  def mobile(self):
    raise AbstractMethodException()

  def killoption(self):
    return Button('Kill').on_click(self.killrequest)
  
  def erroroption(self):
    return Button('Error').on_click(self.errorrequest)
  
  def getoptions(self):
    raise AbstractMethodException()

  def getname(self):
    raise AbstractMethodException()

  def child_died(self, child):
    self.trace.add('child %s died\n' % child)

  def child_errored(self, child, error):
    self.trace.add('child %s errored: %s\n' % (child, error))

  def child_migrated(self, child, to):
    self.trace.add('child %s migrated to: %s\n' % (child, to))

  def killrequest(self, b):
    self.target.kill()
    self.kill()
    
  def errorrequest(self,b ):
    self.target.forceerror()
    self.trace.add('I errored\n')
    
  def imigrated(self, location):
    self.trace.add('I migrated to %s\n' % location)

class RootSupervisorGUI(SupervisionGUI):
  
  def mobile(self):
    return True
  
  def getname(self):
   return "<span color='red'>Root Supervisor</span>"
  
  def getoptions(self):
    return []
    
class SupervisorGUI(SupervisionGUI):
  
  def mobile(self):
    return True
  
  def getname(self):
   return "<span color='blue'>Supervisor</span>"

  def getoptions(self):
    return [self.erroroption()]

class FixedWorkerGUI(SupervisionGUI):
  
  def mobile(self):
    return False
  
  def getname(self):
   return "<span color='green'>Fixed Worker</span>"

  def getoptions(self):
    return [self.killoption(), self.erroroption()]

class MobileWorkerGUI(SupervisionGUI):
  
  def mobile(self):
    return True
  
  def getname(self):
   return "<span color='green'>Mobile Worker</span>"

  def getoptions(self):
    return [self.killoption(), self.erroroption()]