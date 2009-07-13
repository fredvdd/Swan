from Actors.keywords import *
from Actors.Device.GTK.widgets import *
from Actors.Device.GTK.layout import *

class PageEditor(MobileActor):
  
  def birth(self):
    self.textbox = TextView()
    self.htmlview = HtmlView('<body></body>')
    self.textbox.setchangelistener(my('changed'))
    w = Window(HList([ self.textbox, Frame('Preview', self.htmlview)]))
    w.set_size(800, 600)

  def changed(self):
    print self.htmlview.render(self.textbox.contents())