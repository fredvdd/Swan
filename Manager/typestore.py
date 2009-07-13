from collections import defaultdict
from Util.Network import rpc
import Visualizer.client as vis
import threading
import random

class TypeStore(object):
  def __init__(self, overlay):
    self.overlay = overlay
    # Setting default dict type ('set' is {}), makes put a lot nicer
    self.types = defaultdict(set)
    # TODO: use
    self.subtypes = defaultdict(set)

  
  def get_all(self, type, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      return self.types[type]
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      gpids = locator.get_gpids_by_type(type, hash)
      locator.disconnect()
      return gpids

  def get(self, type, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      choices = self.types[type]
      #TODO: Something more intelligent to help balancing
      return random.choice(list(choices))
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      gpid = locator.get_gpid_by_type(type, hash)
      locator.disconnect()
      return gpid

              
  def put(self, type, gpid, hash, old_gpid = None):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if old_gpid and type in self.types:
      self.types[type].discard(old_gpid)
    if self.overlay.id == ideal_id:
      self.types[type].add(gpid)
      vis.store_type(gpid, self.overlay.here)
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      locator.put_gpid_by_type(type, hash, gpid, old_gpid)
      locator.disconnect()
      
  def remove_type(self, type, gpid):
    if type in self.types:
      if len(self.types[type]) == 1:
        del self.types[type]
      else:
        self.types[type] = self.types[type].discard(loc)
      
  def remove_node(self, loc):
    for alias, gpid in self.nodes.iteritems():
      #TODO: Currently broken- search for loc in gpid
      if gpid == loc:
        del self.types[alias]
 
  
  

