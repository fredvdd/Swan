from Actors.keywords import *
from Actors.Device.status import TheatreStatus

class Probe(MobileActor):
  
  def birth(self, server, home, dest):
    self.home = home
    self.dest = dest
    self.data = None
    self.server = server
    migrate_to(dest)

  def arrived(self):
    if self.data == None:
      self.do_probe()
    else:
      callback('done', self.server.processed(self, self.dest, self.data))

  def done(self, any):
    die()

  def do_probe(self):
    self.data = [('Theatre', self.dest),
                 ('Load average', sync(TheatreStatus().loadaverage())),
                 ('Operating System', sync(TheatreStatus().osname())),
                 ('Uptime', sync(TheatreStatus().uptime()))]
    migrate_to(self.home)