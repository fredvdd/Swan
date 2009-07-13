from Util.Network import rpc

class MigrationStore(object):
  def __init__(self, overlay):
    self.overlay = overlay
    self.migrations = dict()
  
  def get(self, old_gpid, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      try:
        return self.migrations[old_gpid]
      except KeyError:
        return None 
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      current_gpid = locator.get_migration(old_gpid, hash)
      locator.disconnect()
      return current_gpid
            
  def put(self, current_gpid, old_gpid, hash):
    (ideal_id, ideal_loc) = self.overlay.get(hash)
    if self.overlay.id == ideal_id:
      self.migrations[old_gpid] = current_gpid
    else:
      network_locator = rpc.RPCConnector(ideal_loc)
      locator = network_locator.connect()
      locator.put_migration(current_gpid, old_gpid, hash)
      locator.disconnect()
      
  def remove_migration(self, old_gpid):
    if old_gpid in self.migrations:
      del self.migrations[old_gpid]
      
  def remove_node(self, loc):
    # Do we ever need to use this?
    pass
