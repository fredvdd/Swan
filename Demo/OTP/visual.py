from Actors.keywords import *
from Actors.OTP.supervision import RootSupervisor, FixedWorker, MobileWorker, Supervisor
from Demo.OTP.supervisiongui import RootSupervisorGUI, SupervisorGUI, FixedWorkerGUI, MobileWorkerGUI

class VisualRootSupervisor(RootSupervisor):
  
  def birth(self):
    RootSupervisor.birth(self)
    self.gui = RootSupervisorGUI(self)
    
  def child_died(self, child):
    self.gui.child_died(child)
    
  def child_errored(self, child, error):
    self.gui.child_errored(child, error)
  
  def child_migrated(self, child, to):
    self.gui.child_migrated(child, to)

  def arrived(self):
    RootSupervisor.arrived(self)
    self.gui.imigrated(here())
    self.gui.migrate_to(here())
    
class VisualSupervisor(Supervisor):
  
  def birth(self, parent):
    Supervisor.birth(self, parent)
    self.gui = SupervisorGUI(self)
    
  def child_died(self, child):
    self.gui.child_died(child)
    
  def child_migrated(self, child, to):
    self.gui.child_migrated(child, to)
    
  def child_errored(self, child, error):
    self.gui.child_errored(child, error)
  
  def forceerror(self):
    None.foo()
    
  def arrived(self):
    Supervisor.arrived(self)
    self.gui.imigrated(here())
    self.gui.migrate_to(here())

class VisualFixedWorker(FixedWorker):
  
  def birth(self, parent):
    FixedWorker.birth(self, parent)
    self.gui = FixedWorkerGUI(self)

  def forceerror(self):
    1/0
    
class VisualMobileWorker(MobileWorker):
  
  def birth(self, parent):
    MobileWorker.birth(self, parent)
    self.gui = MobileWorkerGUI(self)

  def forceerror(self):
    "h" + 1
    
  def arrived(self):
    MobileWorker.arrived(self)
    self.gui.imigrated(here())
    self.gui.migrate_to(here())