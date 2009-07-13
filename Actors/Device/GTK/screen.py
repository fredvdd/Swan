from Actors.keywords import * 
import pygtk
import threading
pygtk.require('2.0')
import gtk
from gtkcanvas import GTKCanvas
from gtkhtmlview import HtmlView
from Actors import native

class Screen(LocalSingletonActor):
  
  def birth(self):
    # Maps actors to the GTK element they represent
    self.widgets = dict()
    # Start a thread for the GUI
    GUIRunner().start()

  def theatreclosing(self):
    gtk.threads_enter()
    # Actor widgets should receive the theatreclosing
    # message first and unregister themselves.  For sanity 
    # we reap any GTK elements which have not been removed
    # by their corresponding actor.
    for widget in self.widgets.values():
      widget.destroy()
    gtk.main_quit()
    gtk.threads_leave()

  def remove(self, windowactor):
     window = self.widgets[windowactor]
     gtk.threads_enter()
     window.destroy()
     del self.widgets[windowactor]
     gtk.threads_leave()
     
  def reg_window(self, actor):
    gtk.threads_enter()
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event", self.ext_delete_event, actor)
    window.set_border_width(10)
    window.show()
    gtk.threads_leave()
    self.widgets[actor] = window
  
  def ext_delete_event(self, widget, event, windowactor):
    # The GTK window itself has no jurisdiction 
    # over whether it should close.  It must inform
    # the Window Actor that a close request has been
    # made but responsibility for closing the window
    # is delegated to the Actor.
    
    # This is a GTK callback so we must use the native interface
    native.send(windowactor, 'close_request')
    return True
  
  def reg_button(self, actor, text):
    gtk.threads_enter()
    button  = gtk.Button(text)
    button.connect("clicked", self.ext_clicked, actor)
    button.show()
    gtk.threads_leave()
    self.widgets[actor] = button
    
  def reg_disabled_button(self, actor, text):
    gtk.threads_enter()
    button  = gtk.Button(text)
    button.set_relief(gtk.RELIEF_NONE)
    button.set_events(0)
    button.unset_flags(gtk.CAN_FOCUS)
    button.show()
    gtk.threads_leave()
    self.widgets[actor] = button

  def reg_htmlview(self, actor, html):
    gtk.threads_enter()
    htmlview = HtmlView(actor)
    htmlview.show()
    gtk.threads_leave()
    self.widgets[actor] = htmlview
    
  def render(self, actor, html):
    gtk.threads_enter()
    self.widgets[actor].display_html(html)
    gtk.threads_leave()
    
  def reg_canvas(self, actor, size):
    gtk.threads_enter()
    drawingarea = GTKCanvas(size)
    drawingarea.show()
    gtk.threads_leave()
    self.widgets[actor] = drawingarea
    
  def mouselisten(self, actor, listener):
    gtk.threads_enter()
  #  self.widgets[actor].mouselisten(listener)
    gtk.threads_leave()
    
  def nomouselisten(self, actor):
    gtk.threads_enter()
   # self.widgets[actor].nomouselisten()
    gtk.threads_leave()
    
  def reg_frame(self, actor, label):
    gtk.threads_enter()
    frame = gtk.Frame(label)
    frame.show()
    gtk.threads_leave()
    self.widgets[actor] = frame
    
  def ext_clicked(self, *args):           
    self.joinactor('clicked', args)
                      
  def clicked(self, gtk, actor):
    actor.clicked()

  def reg_textbox(self, actor, text):
    gtk.threads_enter()
    entry = gtk.Entry(max=0)
    entry.set_text(text)
    entry.connect("changed", self.ext_changed, actor)   
    gtk.threads_leave()
    self.widgets[actor] = entry
    
  def reg_textview(self, actor, text):
    gtk.threads_enter()
    textview = gtk.TextView()
    textview.get_buffer().set_text(text)
    textview.get_buffer().connect("changed", self.ext_view_changed, actor)   
    gtk.threads_leave()
    self.widgets[actor] = textview
  
  def ext_view_changed(self, *args):
     self.joinactor('viewchanged', args)
  
  def viewchanged(self, buffer, actor):
    actor.nofify_text_changed(buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter()))
  
  def ext_changed(self, *args):
    self.joinactor('changed', args)
     
  def changed(self, gtk, actor):
    actor.nofify_text_changed(gtk.get_text())
     
  def reg_label(self, actor, text):
    gtk.threads_enter()
    label = gtk.Label()
    label.set_markup(text)
    gtk.threads_leave()
    self.widgets[actor] = label

  def reg_hbox(self, actor, hom):
    gtk.threads_enter()
    hbox = gtk.HBox(homogeneous=hom, spacing=0)
    hbox.show()
    gtk.threads_leave()
    self.widgets[actor] = hbox
    
  def reg_vbox(self, actor, hom):
    gtk.threads_enter()
    hbox = gtk.VBox(homogeneous=hom, spacing=0)
    hbox.show()
    gtk.threads_leave()
    self.widgets[actor] = hbox
    
  def reg_vpair(self, actor):
    gtk.threads_enter()
    vbox = gtk.VBox(homogeneous=False, spacing=0)
    vbox.show()
    gtk.threads_leave()
    self.widgets[actor] = vbox
    
  def set_size(self, actor, hsize, vsize):
    gtk.threads_enter()
    self.widgets[actor].resize(hsize, vsize)  
    gtk.threads_leave()
    
  def get_size(self, actor):  
    gtk.threads_enter()
    size = self.widgets[actor].get_size()
    gtk.threads_leave()
    return size
    
  def packstart(self, parent, child, expand):  
    gtk.threads_enter()
    gtk_parent =  self.widgets[parent]
    gtk_child = self.widgets[child]
    gtk_parent.pack_start(gtk_child, expand=expand, fill=True, padding=0)
    gtk_child.show()
    gtk.threads_leave()
    
  def packend(self, parent, child):  
    gtk.threads_enter()
    gtk_parent =  self.widgets[parent]
    gtk_child = self.widgets[child]
    gtk_parent.pack_end(gtk_child, expand=False, fill=False, padding=0)
    gtk_child.show()
    gtk.threads_leave()
    
  def add(self, parent, child):
    gtk.threads_enter()
    gtk_parent =  self.widgets[parent]
    gtk_child = self.widgets[child]
    gtk_parent.add(gtk_child)
    gtk.threads_leave()

  def set_markup(self, actor, text):
    gtk.threads_enter()
    self.widgets[actor].set_markup(text)
    gtk.threads_leave()
  
  def set_pos(self, actor, xalign, yalign):
    gtk.threads_enter()
    self.widgets[actor].set_alignment(xalign, yalign)
    gtk.threads_leave()

  def set_text(self, actor, text):
    gtk.threads_enter()
    self.widgets[actor].set_text(text)
    gtk.threads_leave()
    
  def draw_line(self, actor, (x1, y1, x2, y2)):
    gtk.threads_enter()
    widget = self.widget(actor)
    if widget:
      widget.draw_line(x1, y1, x2, y2)
    gtk.threads_leave()
    
  def widget(self, actor):
    if self.widgets.has_key(actor):
      return self.widgets[actor]
    return None
  
  def draw_rect(self, actor, (x1, y1, x2, y2)):
    gtk.threads_enter()
    widget = self.widget(actor)
    if widget:
      widget.draw_rect(x1, y1, x2, y2)
    gtk.threads_leave()
    
  def commit(self, actor):
    gtk.threads_enter()
    self.widgets[actor].commit()
    gtk.threads_leave()
  
  def clear(self, actor):
    gtk.threads_enter()
    self.widgets[actor].clear()
    gtk.threads_leave()

class GUIRunner(threading.Thread):
  
  def run(self):
    gtk.gdk.threads_init()
    gtk.main()

