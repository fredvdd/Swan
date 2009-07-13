from Util.Network import rpc
import time
import threading
import Visualizer.client as vis

class NameStore(object):
  def __init__(self, overlay):
    self.overlay = overlay
    self.names = dict()
    self.singleton_cond = threading.Condition()
    self.current_reg = set()

  def clever_lock_get(self, name):
    """Locks by name"""
    got = False
    while not got:
      self.singleton_cond.acquire()
      if name not in self.current_reg:
        self.current_reg.add(name)
        self.singleton_cond.release()
        got = True
      else:
        self.singleton_cond.release()
        time.sleep(0.02)            
  
  def clever_lock_release(self, name):
#    self.singleton_cond.acquire()
    self.current_reg.remove(name)
#    self.singleton_cond.release()
  
  def get(self, alias, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      return self.names[alias]
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      gpids = locator.get_gpid_by_name(alias, hash)
      locator.disconnect()
      return gpids
            
  def put(self, alias, gpid, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      self.names[alias] = gpid
      vis.store_name(alias, gpid, self.overlay.here)
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      locator.put_gpid_by_name(alias, hash, gpid)
      locator.disconnect()
      
      
  def create_named_singleton(self, alias, suggested_loc, actor_info, hash):
      (ideal_id, ideal_loc) = self.overlay.get(hash)
      if self.overlay.id == ideal_id:
       self.clever_lock_get(alias)
       exists = (alias in self.names)
       if exists:
         self.clever_lock_release(alias)
         return (self.names[alias], exists)
       else:
         network_locator = rpc.RPCConnector(suggested_loc)
         locator = network_locator.connect()
         gpid = locator.create_actor(*actor_info)
         locator.disconnect()
         self.names[alias] = gpid
         self.clever_lock_release(alias)
         vis.store_name(alias, gpid, self.overlay.here)
      else:
        network_locator = rpc.RPCConnector(ideal_loc)
        locator = network_locator.connect()
        (gpid, exists) = locator.create_named_singleton(alias, suggested_loc, actor_info, hash)
        locator.disconnect()
      return (gpid, exists)
      
  def remove_node(self, alias):
    if alias in self.names:
      del self.names[alias]
      
  def remove_node(self, loc):
    for alias, gpid in self.nodes.iteritems():
      #TODO: Currently broken- search for loc in gpid
      if gpid == loc:
        del self.names[alias]