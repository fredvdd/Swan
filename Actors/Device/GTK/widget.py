from Actors.keywords import * 
from Actors.Device.GTK.screen import Screen

class WindowWidget(MobileActor):
  
  def birth(self):
    self.screen = None
    self.migrate_on_close = False
  
  def keepalive(self):
    self.migrate_on_close = True
  
  def migrate_to(self, theatre):
    migrate_to(theatre)
      
  def set_size(self, hsize, vsize):
    self.hsize = hsize
    self.vsize = vsize
    self.update()
  
  def update(self):  
    pass

  def unregister(self):
    if self.screen:
      sync(self.screen.remove(self))
    self.screen = None
  
  def kill(self):
    die()
    
  def theatreclosing(self):
    self.screen = None
    if self.migrate_on_close: 
      migrate_or_die()
    
class ContainerWidget(WindowWidget):
  
  def birth(self, children):
    WindowWidget.birth(self)
    self.children = children

  def unregister(self):
    sync([child.unregister() for child in self.children])
    WindowWidget.unregister(self)
  
  def keepalive(self):
    self.migrate_on_close = True
    for child in self.children:
      child.keepalive()
  
  def update(self):
    sync([child.update() for child in self.children])
    
  def arrived(self):
    for child in self.children:
      child.migrate_to(here())
      
  def kill(self):
    [child.kill() for child in self.children]
    WindowWidget.kill(self)