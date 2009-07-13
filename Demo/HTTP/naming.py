from Actors.keywords import *

class NameServer(NetworkSingletonActor):
  
  def birth(self):
    self.servers = dict()
    
  def lookup(self, hostname):
    if hostname in self.servers:
      return self.servers[hostname]
    return None
    
  def register(self, server, hostname):
    self.servers[hostname] = server