import pygtk
pygtk.require('2.0')
import gtk
from eventinterface import Mouse
from Actors import native

class GTKCanvas(gtk.DrawingArea):
  """A am a simple drawing canvas which allows simple
     animation using rectangles and lines"""
  
  def __init__(self, size):
    gtk.DrawingArea.__init__(self)
    self.connect("expose_event", self.expose_event)
    self.connect("configure_event", self.configure_event)
    self.set_events(gtk.gdk.EXPOSURE_MASK)
    self.set_flags(gtk.CAN_FOCUS)
    self.mysize = size
    self.set_size_request(size[0], size[1])
    self.px = None
    
  def mouselisten(self, actor):
    """Sets 'actor' as the target for mouse move
       messages.  Adding a listener will cause a 
       non-trivial number of messages to be sent"""
  
  # Mouse events disabled to poor performance.
  
  #  self.mouse = Mouse(actor)
    
  #  self.set_events(gtk.gdk.EXPOSURE_MASK
  #                | gtk.gdk.POINTER_MOTION_MASK
  #                | gtk.gdk.POINTER_MOTION_HINT_MASK)
  #  
  #  self.connect("motion_notify_event", self.motion_notify, None)
  
  def nomouselisten(self):
    """Removes the mouselistener"""
    #self.mouse.kill()
    
  def motion_notify(self, widget, event, actor):
    """GTK callback, called on mousemove""" 
    if event.is_hint:
        x, y, state = event.window.get_pointer()
    else:
        x = event.x
        y = event.y
    # Use the device to actor message sending interface    
    # Re-normalise the coordinates to place the origin
    # in the bottom left corner - this makes animation
    # coordinates more intuative
    #  native.send(self.mouse, 'mousemove', x, self.mysize[1] - y)
    return True
  
  def __newbuffer(self, width, height):
    """Creates a new backing bufer"""  
    map = gtk.gdk.Pixmap(self.window, width, height)
    map.draw_rectangle(self.get_style().white_gc,True, 0, 0, width, height)
    return map
    
  def draw_line(self, x1, y1, x2, y2):
    if self.px:
      self.px.draw_line(self.get_style().black_gc, x1, y1, x2, y2)

  def draw_rect(self, x, y, width, height):
    style = self.get_style()
    if self.px and style:
      self.px.draw_rectangle(style.black_gc, True, x, y, width, height)

  def configure_event(self, widget, event):
    x, y, width, height = widget.get_allocation()
    self.px = self.__newbuffer(width, height)
    return True
    
  def expose_event(self, widget, event):
    if self.px:
      x , y, width, height = event.area
      self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL], self.px, x, y, x, y, width, height)
    return True
    
  def clear(self):
    if self.px:
     (width, height) = self.window.get_size()
     self.px.draw_rectangle(self.get_style().white_gc,True, 0, 0, width, height)
     
  def commit(self):
    style = self.get_style() 
    if self.px and style:
      (width, height) = self.window.get_size()
      self.queue_draw_area(0, 0, width, height)