from Actors.keywords import * 
from screen import Screen
from widget import ContainerWidget
import time

class Canvas(ContainerWidget):
  
  def birth(self, size):
    ContainerWidget.birth(self, [])
    self.size = size
    self.screen = None
    self.rects = []
    self.lines = []
    self.mouselistener = None
    
  def getsize(self):
    return self.size
    
  def mouselisten(self, listener):
    pass
    #self.mouselistener = listener
    #if self.screen:
    #  screen.mouselisten(self, self.mouselistener)
      
  def mousemove(self, x, y):
    pass

  def register(self, screen):
    self.screen = screen
    sync(screen.reg_canvas(self, self.size))
    #if self.mouselistener:
    #  sync(screen.mouselisten(self, self.mouselistener))
    
  def line(self, x1, y1, x2, y2):
    line = Line(self, x1, y1, x2, y2)
    self.lines.append(line)
    self.update()
    return line
  
  def add(self, rect):
    self.rects.append(rect)
    self.update()
  
  def remove_child(self, rect):
    if rect in self.rects:
      self.rects.remove(rect)
      self.update()
  
  def intersection(self):
    pass
  
  def update(self):
    if self.screen:
      intersection = False
      maxy = self.size[1]
      items = sync([rect.getspec() for rect in self.rects])
      sync(self.screen.clear(self))
      sync([self.screen.draw_rect(self, (x, maxy - y + 1 - h, w, h)) for (x, y, w, h) in items])     
      sync(self.screen.commit(self))
      if test_intersections(items):
        self.intersection()
    
  def unregister(self):
    if self.screen and self.mouselistener:
      sync(self.screen.nomouselisten(self))
    ContainerWidget.unregister(self)
    
  def arrived(self):
    for rect in self.rects:
      rect.migrate_to(here())

class Line(MobileActor):
  
  def birth(self, canvas,  x1, y1, x2, y2):
    self.p1 = (x1, y1)
    self.p2 = (x2, y2)
    self.canvas = canvas
    
  def getspec(self):
    return self.p1 + self.p2
  
def test_intersections(items):
  for item1 in items:
    matched = 0
    for item2 in items:
      if intersects(item1, item2):
        matched += 1
    if matched > 1:
      return True
  return False  
  
def intersects((x1, y1, w1, h1), (x2, y2, w2, h2)): 
  return x2 >= x1 and x2 <= x1+w1 and y2 >= y1 and y2 <= y1+h1 
  
class Rect(MobileActor):
  
  def birth(self, canvas, x, y, width, height):
   self.left = (x,y)
   self.size = (width, height)
   self.canvas = canvas
   if self.canvas:
     self.canvas.add(self)
     self.canvas.update()
   
  def setpos(self, x, y):
   self.left = (x, y)
   if self.canvas:
     self.canvas.update()

  def delete(self):
    if self.canvas:
      callback('removed', self.canvas.remove_child(self))
    
  def removed(self, result):
    pass
    #die()

  def attach(self, canvas):
    self.canvas = canvas
    self.canvas.add(self)
    self.canvas.update()

  def detach(self):
    if self.canvas:
      self.canvas.remove_child(self)
  
  def attached_to(self):
    return self.canvas

  def migrate_to(self, theatre):
    migrate_to(theatre)
  
  def getspec(self):
    return self.left + self.size