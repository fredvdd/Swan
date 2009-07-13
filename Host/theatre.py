from Migration.migrator import Migrator
from external import TheatreExternalInterface
from internal import TheatreInternalInterface
from messenger import Messenger
from actorstore import LocalActorStore
from static import log, set_local_theatre
from Util.Network import rpc
import time
import os
import Util.ids as ids
from terminal import Terminal
import Visualizer.client as vis
import sys

try:
  import multiprocessing as mp
  if mp.cpu_count() > 1:
    from shared import Shared
  else:
    from sharedbyone import Shared
except ImportError:
  from sharedbyone import Shared


class Theatre(object):
   
  def __init__(self, here, manager_loc, core_store, store_lock, current_id, id_lock, current_creator, creator_lock, port_range, f = None, ps = None):
    log.debug(self, 'starting')
    self.__here = here
    port = ids.port_from_loc(here)
    self.__shared_data = Shared(port, current_id, id_lock, core_store, store_lock, current_creator, creator_lock, port_range)    
    self.__actor_store = LocalActorStore(self.__here, self.__shared_data)
    self.__messenger = Messenger(here, self.__actor_store)
    self.__migrator = Migrator(here, self.__actor_store, self.__shared_data)
    self.__manager_loc = manager_loc
    self.__port_range = port_range
    self.__term = None
    self.__processes = ps
 
    if (port == port_range[0]):
      self.__term = Terminal(self, here)
    self.valve = rpc.RPCValve(port, self.external_interface(), log)
    set_local_theatre(self.internal_interface())
    self.valve.listen()
    print('Theatre created on port ' + str(port))
    
    vis.add_host(here)
              
    if (port != port_range[0]):
      while True:
        try:
          time.sleep(5)
        except:
          pass

    else:
      self.f = f
      self.f()
      self.__term.shell()
   
  def external_interface(self):
     return TheatreExternalInterface(self.__messenger, self.__migrator, self.__term, self, self.__actor_store)
   
  def internal_interface(self):
    return TheatreInternalInterface(self.__here, self.__messenger, self.__actor_store, self.__migrator, self.__manager_loc, self.__shared_data)
  
  def shutdown(self):
    for port in self.__port_range:
      if (port != self.__port_range[0]):
        network_locator = rpc.RPCConnector("127.0.0.1:" + str(port))
        locator = network_locator.connect()
        locator.shutdown()
        locator.disconnect()
    self.valve.shutdown()
    time.sleep(2)
    for p in self.__processes:
      p.terminate()
    time.sleep(2)        
    sys.exit()
    
  def __str__(self):
    return "Theatre" 
