from Util.Network import rpc
import diskinterface
import sys
import os

class ScriptStore(object):
  def __init__(self, overlay):
    self.overlay = overlay
    self.files = dict()
  
  def get(self, module_name, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      # TODO: thow exceptions
      self.files[module_name] = name
      src = self.get_from_disk(filename)
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      gpids = locator.get_script(alias, hash)
      locator.disconnect()
      return src
            
  def put(self, module_name, src, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      name = self.save_to_disk(module_name, src)
      self.files[module_name] = name
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      locator.put_script(alias, module_name, src, hash)
      locator.disconnect()
      
  def put_locally(module_name, src):
    name = self.save_to_disk(module_name, src)
    self.files[module_name] = name
    return name
      
  def exists(self, module_name, hash): 
    # TODO: dubious first case- file may not be where we expect
    if module_name in self.files:
      return (True, self.overlay.here)
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      return (module in self.files, self.overlay.here)
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      exists = locator.script_exists(module_name, hash)
      locator.disconnect()
      return exists

      
  def remove_name(self, alias):
    if alias in self.names:
      del self.names[alias]
      
  def remove_node(self, loc):
    for alias, gpid in self.nodes.iteritems():
      #TODO: Currently broken- search for loc in gpid
      if gpid == loc:
        del self.names[alias]
 

