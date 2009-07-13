from Actors.keywords import *
from Demo.Yapper.person import Person
from Actors.Device.input import Keyboard
import Util.ids 

class Client(MobileActor):
  def birth(self):
    Keyboard().listen(self.shell)
    print "commands:\n\t l (user) \t log in as the given user \n\t q \t\t quit"
    self.attached = None

  def shell(self, command):
    opt = command[0:2] 
    param = command[2:len(command)]
    if opt == "l ":
      self.attached = Person(param)
      here = ids.loc(self.actor_id)
      self.attached.attach(param, here)
      self.help()
    if opt == "q":
       if self.attached is not None:
         self.attached.migrate_away()
       die()
    if opt == "w" and self.attached is not None:
      self.attached.print_wall()
    if opt == "y " and self.attached is not None:
      self.attached.yap(param)
    if opt == "f " and self.attached is not None:
        self.attached.follow(param)
    if opt == "h":
      self.help()

  def help(self):
    print "commands:\n\tw \t\t print wall \n\t\
y (message) \t yip a message \n\tf (user) \t Follow the given user \n\t\
h \t\t print this help message \n\tq \t\t quit"

def start():
  Client()

if __name__ == '__main__':
  initialise(start)
