from Actors.keywords import *
from Actors.Device.GTK.widgets import *
from Actors.Device.GTK.layout import *
from Demo.HTTP.Browser.errorpages import *

class BrowserWindow(Window):
  
  def birth(self, events):
    self.events = events
    
    htmlview = HtmlView(SPLASHSCREEN).on_link_click(self.link_clicked)
    Window.birth(self, VPair(Frame('Rendered page', htmlview), 
                             NavBar(events)))
    
    events.subscribe('render', htmlview.render)
  
  def link_clicked(self, url):
     self.events.publish('url_requested', url)
  
class NavBar(Frame):
    
  def birth(self, events):
    self.events = events
    self.textbox = TextBox()
    self.textbox.set_text('meta:home')
    go_button = Button('GO').on_click(self.navigate)
    Frame.birth(self, 'Navigation', HPair(self.textbox, go_button))
    events.subscribe('url_requested', self.textbox.set_text)
  
  def navigate(self, button):
    self.events.publish('url_requested', self.textbox.contents())