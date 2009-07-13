from Actors.keywords import *
from Actors.Device.GTK.widgets import *
from Actors.Device.GTK.layout import *
from Actors.Device.input import Keyboard

class User(NetworkActor):
  
  def birth(self, name, color):
    self.name = name
    self.color = color
    self.server = ChatServer()
    sync(self.server.add(self))
    
  def send(self, message):
    self.server.say(self.name, self.color, message) 
      
  def incoming(self, name, color, message):
    self.show_message(name, color, message)

class ChatServer(NetworkSingletonActor):
  
  def birth(self):
    self.chatters = []
    
  def add(self, person):
    self.chatters.append(person)
    
  def say(self, name, color, message):
    for chatter in self.chatters:
      chatter.incoming(name, color, message)  

class GUIUser(User):
  
  def birth(self, name, color):
    User.birth(self, name, color)
    
    self.message_pad = Label('')
    self.input = TextBox()
    button = Button('send').on_click(self.clicked)
   
    self.w = Window(VPair(self.message_pad, 
                     HPair(self.input, button)))
    self.w.set_size(400, 200)
    
  def show_message(self, name, color, string):
    formatted = "<span foreground='%s'><b>%s:</b></span> %s\n" % (color, name, string)  
    sync(self.message_pad.add(formatted))
    sync(self.input.clear())
    
  def clicked(self, button):
    string = sync(self.input.contents())
    self.send(string)
  
class ConsoleUser(User):
  
  def birth(self, name, color):
    User.birth(self, name, color)
    Keyboard().readline(Reference(self.actor_id))
    
  def userwrote(self, string):
    self.send(string)
    Keyboard().readline(Reference(self.actor_id))
    
  def show_message(self, name, color, message):
    print "%s: %s" % (name, message)
