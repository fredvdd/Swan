from Util import exceptions
from Util.Network import rpc
from Actors.actor import Actor
from Host.static import local_theatre, log
import inspect
import sys
import Util.ids as ids

class Migrator(object):
  
  def __init__(self, theatreaddress, local_actor_store, shared_data):
    self.__local_actor_store = local_actor_store
    self.here = theatreaddress
    self.shared_data = shared_data
      
  def migrate_to(self, actor, address):
     print 'in migrator'
     log.debug(self, 'about to migrate %s to %s' % (actor, address))
     
     if address == local_theatre().gethostname():
       # Still add an arrive message since the actor requested a local
       # migration and may be relying the arrived notification
       actor.state.add_arrived()
       log.debug(self, 'pointless (local) migration')
       return True
     # Inform the local locator that the actor cannot service any
     # further requests on this host
     self.__local_actor_store.remove(actor.state.actor_id)
#     try:
     self.__migrate_remote(actor, address)
#     except:
#       return False
     # Stop the actor's process loop
     actor.stop()
     log.debug(self, 'stopped local runner for actor %s' % actor)
     return True
     
  def __migrate_remote(self, actor, address):
     module = actor.getmodule()
     modulename = module.__name__
   
     if modulename == '__main__':
       raise Exception('Cannot migrate actors defined in the main module')

     if ids.ip_from_loc(self.here) != ids.ip_from_loc(address):
       # Non-local migration
       src = inspect.getsource(module)
       local_theatre().store_script(module.__name__, src)
       conn = rpc.RPCConnector(address)
       remote_theatre = conn.connect()
       remote_theatre.get_script(modulename)
       remote_theatre.disconnect()
           
     conn = rpc.RPCConnector(address)
     actor.state.add_arrived()
     remote_theatre = conn.connect()
     remote_theatre.incoming_actor(actor.state)
     remote_theatre.disconnect()
     
  def get_script(self, module_name):
    if sys.modules.has_key(module_name):
      return
    try:
      __import__(module_name)
      return
    except:
      self.__lock.release()
      path = local_theatre().import_script(module_name)      
      imp.acquire_lock()
      imp.load_source(modulename, path)
      imp.release_lock()
      return

  def atheatre(self):
    return self.__locator.atheatre()

  def __str__(self):
    return "Migrator"
  
  def incoming_actor(self, actorstate):
    # Create actor but don't start
    # TODO: FIX- generation of id, handle local and non-local migrations.
    log.debug(self, 'receieved migrating actor %s' % actorstate)
    actor = Actor(local_theatre())
    actor.state = actorstate
    old_actor_id = actor.state.actor_id 
    type = actor.state.actortype
    if ids.ip(old_actor_id) == ids.ip_from_loc(self.here):
      # Migration has been local
      actor_id = ids.change_port(old_actor_id, ids.port_from_loc(self.here))
    else:
      actor_id = ids.change_host(old_actor_id, self.here, self.shared_data.next_id_num())

    actor.state.actor_id = actor_id
    self.__local_actor_store.add_network_actor(actor, actor_id)
    actor.start()
    # At the moment even core migrations trigger re-registrations
    # Could probably forgo these if core migrations are frequent.
    local_theatre().globally_reregister_network_actor(actor_id, type, old_actor_id)
    names = actor.state.names
    for name in names:
      local_theatre().name(name, actor_id)
    
    
