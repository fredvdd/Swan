from Actors.keywords import *
from Actors.Device.GTK.widgets import *
from target import Target

class GUI(MobileActor):
  
  def birth(self):
    display = Label('')
    migrate_button = Button('migrate').on_click(self.clicked)
    self.window = Window(VPair(VPair(display, Editor(display)), migrate_button))
    self.window.set_size(400, 400)
    
  def clicked(self):
    next = sync(GUIList().nexthost())
    migrate_to(next)
  
  def arrived(self):
    self.window.migrate_to(here())


class Editor(TextView):
  
  def birth(self, display):
    TextView.birth(self)
    self.display = display
  
  def modified(self):
    self.display.set_text(self.contents()) 

class GUIList(NetworkSingletonActor):
  
  def birth(self):
    self.hosts = []
    self.index = 0
    
  def addhost(self, host):
    self.hosts.append(host)
    if len(self.hosts) == 1:
      return True
    return False
    
  def nexthost(self):
    next = self.hosts[self.index]
    self.index = (self.index + 1) % len(self.hosts)
    return next