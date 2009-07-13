from Actors.keywords import * 
from Actors.Device.GTK.screen import Screen
from Actors.Device.GTK.widget import WindowWidget, ContainerWidget

class Window(LocalActor):
  
  def birth(self, child):
    self.child = child
    self.hsize = 200
    self.vsize = 200
    self.migrate_on_close = False
    self.closehandler = None
    self.localise()

  def close_request(self):
    if self.closehandler:
      self.closehandler(self)
      
  def set_closehandler(self, handler):
    self.closehandler= handler

  def set_size(self, hsize, vsize):
    self.hsize = hsize
    self.vsize = vsize
    sync(self.screen.set_size(self, hsize, vsize))
    sync(self.child.set_size(hsize, vsize))
     
  def keepalive(self):
    self.migrate_on_close = True
    self.child.keepalive()
     
  def migrate_to(self, newlocation):
    sync(self.child.unregister())
    sync(self.screen.remove(self))
    migrate_to(newlocation)

  def arrived(self):
    self.child.migrate_to(here())
    self.localise()
   
  def localise(self):  
    self.screen = screen = Screen()
    sync(screen.reg_window(self))
    sync(self.screen.set_size(self, self.hsize , self.vsize))
    sync(self.child.set_size(self.hsize, self.vsize))
    sync(self.child.register(screen))
    sync(screen.add(self, self.child))
    sync(self.child.update())

  def kill(self):
    self.child.unregister()
    self.screen.remove(self)
    self.child.kill()
    die()
    
  def theatreclosing(self):
    self.screen = None
    if self.migrate_on_close:
      migrate_or_die()

class DisabledButton(WindowWidget):
 
  def birth(self, title):
    WindowWidget.birth(self)
    self.title = title
    
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_disabled_button(self, self.title))
              
  def get_title(self):
    return self.title  

class Button(WindowWidget):
 
  def birth(self, title):
    WindowWidget.birth(self)
    self.title = title

  def on_click(self, target):
    self.target = target
    return self
    
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_button(self, self.title))
              
  def clicked(self):
    self.target(self)
  
  def get_title(self):
    return self.title
              
class TextBox(WindowWidget):
 
  def birth(self):
    WindowWidget.birth(self)
    self.text = ''
     
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_textbox(self, self.text))
   
  def contents(self):
    return self.text 
  
  def clear(self):
    self.set_text('')
    self.update()
  
  def nofify_text_changed(self, text):
    self.text = text
  
  def set_text(self, text):
    self.text = text
    self.update()
      
  def update(self):
    if self.screen:
      sync(self.screen.set_text(self, self.text))
    
class TextView(WindowWidget):
 
  def birth(self):
    WindowWidget.birth(self)
    self.text = ''
    self.listener = None
     
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_textview(self, self.text))

  def nofify_text_changed(self, text):
    self.text = text
    self.modified()
 
  def setchangelistener(self, listener):
    self.listener = listener
   
  def modified(self):
    if self.listener:
      self.listener()
   
  def contents(self):
    return self.text 
  
  def set_text(self, text):
    self.text = text
    if self.screen:
      sync(self.screen.set_markup(self, text))
    
class HtmlView(WindowWidget):
 
  def birth(self, html):
    self.linkhandler = None
    self.html = html
    WindowWidget.birth(self)
    
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_htmlview(self, self.html))

  def render(self, html):
    self.html = html
    self.update()

  def update(self):
    if self.screen:
      sync(self.screen.render(self, self.html))

  def on_link_click(self, handler):
    self.linkhandler = handler
    return self

  def link_clicked(self, url):
    if self.linkhandler:
      self.linkhandler(url)
    
class Label(WindowWidget):
  
  def birth(self, text):
    WindowWidget.birth(self)
    self.text = text
    
  def set_text(self, text):
    self.text = text
    self.update()
    
  def add(self, text):
    self.text += text
    self.update()
    
  def update(self):
    if self.screen:
      self.screen.set_markup(self, self.text)
    
  def register(self, screen):
    self.screen = screen
    sync(screen.reg_label(self, self.text))
    sync(screen.set_pos(self, 0, 0))