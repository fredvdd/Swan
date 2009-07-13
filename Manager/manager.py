from external import ManagerExternalInterface
from Util.Network import rpc
from Util.Network import ipfinder
from Util import signalutil
from managerlog import log
from socket import gethostname
from overlay import Overlay
from namestore import NameStore
from typestore import TypeStore
from migrationstore import MigrationStore
from scriptstore import ScriptStore
import Visualizer.client as vis
import socket
import sys


DEFAULT_MANAGER_PORT = 7000

class Manager(signalutil.Runner):

  def __init__(self, port=DEFAULT_MANAGER_PORT):
    signalutil.Runner.__init__(self)
    self.port = port
    self.overlay = Overlay()
    self.name_store = NameStore(self.overlay)
    self.type_store = TypeStore(self.overlay)
    self.migration_store = MigrationStore(self.overlay)
    self.script_store = ScriptStore(self.overlay)
        
  def begin(self):
    loc = ManagerExternalInterface(self.overlay, self.name_store, self.type_store, self.migration_store, self.script_store)
    port = self.port
    while (port < self.port + 10):
      if self.takeport(port, loc):
        self.port = port
        break
      port = port + 1;
    log.debug(self, 'listening on port %s' % port) 
    here = socket.gethostbyname(socket.gethostname()) + ':%d' % self.port
    ipfinder.create_ip_server(DEFAULT_MANAGER_PORT - 1)
    self.overlay.here(here)
    self.overlay.populate(sys.argv)
    vis.add_manager(here)
    self.shell()

  def takeport(self, port, loc):
    try:
      self.__valve = rpc.RPCValve(port, loc, log)
      self.__valve.listen()
      return True
    except socket.error:
      return False
      
  
  def shutdown(self):
    log.debug(self, 'shutting down')
    try:
      self.__valve.shutdown()
      print 'closing port'
    except socket.error as e:
      print 'ERROR:', e.args
      
      
  def __str__(self):
    return 'Manager'
    
  def shell(self):
    print 'Welcome to Stage#'
    execute = True
    while execute:
      if True:
        print (gethostname() + ':%d>' % self.port),
        command = sys.stdin.readline().strip()
        if command == 'exit':
          execute = False
        else: 
          try:
            exec(command)
          except:
            print 'command not found'
    self.shutdown()
    sys.exit()
    
if __name__ == '__main__':
  Manager().start()
