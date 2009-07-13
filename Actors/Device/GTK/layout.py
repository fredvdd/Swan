from Actors.keywords import *
from widget import ContainerWidget, WindowWidget

class Frame(ContainerWidget):
  
  def birth(self, label, child):
    self.label = label
    ContainerWidget.birth(self, [child])

  def register(self, screen): 
    self.screen = screen 
    sync(screen.reg_frame(self, self.label))
    sync(self.children[0].register(screen))
    sync(screen.add(self, self.children[0]))

class List(ContainerWidget):
  
  def birth(self, children):
    ContainerWidget.birth(self, children)
    self.homogenious = True
 
  def register(self, screen): 
    self.screen = screen 
    self.register_self()
    sync([child.register(screen) for child in self.children])
    sync([screen.packstart(self, child, self.homogenious) for child in self.children])      
    
  def dontequalise(self):
    self.homogenious = False
  
  def clear(self):
    sync([child.unregister() for child in self.children])
    for child in self.children:
      child.kill()
    self.children = []
      
  def add(self, child):
    self.children.append(child)
    if self.screen:
      sync(child.register(self.screen))
      sync(self.screen.packstart(self, child, self.homogenious))

class HList(List):
  
  def register_self(self):
    sync(self.screen.reg_hbox(self, self.homogenious))
  
class VList(List):
  
  def register_self(self):
    sync(self.screen.reg_vbox(self, self.homogenious))
 
class Pair(ContainerWidget):
  
  def birth(self, first, second):
    ContainerWidget.birth(self, [first, second])

  def register(self, screen): 
    self.screen = screen 
    self.register_self()
    sync(self.children[0].register(screen))
    sync(self.children[1].register(screen))
    sync(screen.packstart(self, self.children[0], True))
    sync(screen.packend(self, self.children[1]))
  
  def setsecond(self, second):
    oldsecond = self.children[1]
    sync(oldsecond.unregister())
    self.children[1] = second
    if self.screen:
      sync(self.children[1].register(self.screen))
      sync(self.screen.packend(self, self.children[1]))
    oldsecond.kill()
    
class HPair(Pair):

  def register_self(self):
    sync(self.screen.reg_hbox(self, False))
    
class VPair(Pair):
  
  def register_self(self):
     sync(self.screen.reg_vpair(self))