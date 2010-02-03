from Manager.hashing import hash
from Util.Network import rpc
from Actors.actor import Actor
from Actors.reference import Reference
from Actors.referencepool import ReferencePool
import random
import sys
import Util.ids as ids
from Util.exceptions import ActorsOfTypeNotFoundException
import threading
import inspect
import Visualizer.client as vis

class TheatreInternalInterface(object):
  """I represent the low-level operations that a local actor
     may peform.  Stage programmers should not call these
     methods directly rather they should use the relevant syntax as defined
     in the keywords module"""
     
  def __init__(self, hostname, messenger, actor_store, migrator, manager_loc, shared_data):

    self.__hostname = hostname
    self.__port = ids.port_from_loc(self.__hostname)
    self.__messenger = messenger
    self.__local_store = actor_store
    self.__migrator = migrator
    self.__manager_loc  = manager_loc
    self.__shared_data = shared_data
  
  def where_to_create(self):
    port = self.__shared_data.next_port()
    return ids.ip_from_loc(self.__hostname) + ":" + str(port)
    
  def create_actor(self, cls, module_name, type, args, kwds):
    # TODO get lock when creating static actors on core
    if cls.static:
      # No parallism with identical actors in the same process (blame the GIL)
      actor_id = self.__local_store.get_type(type)
      if actor_id:
        return
    id_num = self.__shared_data.next_id_num()
    actor_id = ids.generate(self.__hostname, type, id_num)
    if not sys.modules.has_key(module_name):
      __import__(module_name)
    actor = Actor(self)
    actorstate = object.__new__(cls)
    actorstate.__init__(type, actor_id)
    actorstate.add_birth(args, kwds)
    actor.setstate(actorstate)
    actor.start()
    vis.add_actor(actor_id)
    self.__local_store.add_network_actor(actor, actor_id)
    threading.Timer(0, self.globally_register_network_actor, (actor_id, type)).start()
    return actor_id
    
  def gethostname(self):
    return self.__hostname
  
  def getport(self):
	return self.__port
  
  def get_pool(self, cls):
    ports = self.__shared_data.port_range
    type = cls.__name__
    actor_ids = list()
    if cls.static:
      # Return an actor of this type for every core of this node
      module_name = inspect.getmodule(cls).__name__
      for port in ports:
        if port == self.__port:
          actor_id = self.create_actor(cls, module_name, type, [], dict())
        else:
          network_locator = rpc.RPCConnector(ids.ip_from_loc(self.__hostname) + ':' + str(port))
          core = network_locator.connect()
          actor_id = core.create_actor(cls, module_name, type, [], dict())
          core.disconnect()
        actor_ids.append(actor_id)
    else:
      # Return all actors of this type that exist on this node
      for port in ports:
        if port == self.__port:
          actor_ids.extend(self.__local_store.get_types(type))
        else:
          network_locator = rpc.RPCConnector(ids.ip_from_loc(self.__hostname) + str(port))
          core = network_locator.connect()
          core_actor_ids = core.get_types(type)
          core.disconnect()
          actor_ids.extend(core_actor_ids)
      if len(actor_ids) == 0:
        actor_ids = self.find_all_types(type)
        # TODO: No balancing done in this case
        if len(actor_ids) == 0:
          raise ActorsOfTypeNotFoundException(type)
        return ReferencePool(actor_ids)
    threading.Timer(0, self.notify_types, (actor_ids, type)).start()
    return ReferencePool(actor_ids)

  def notify_types(self, already_using, type):
    ids = self.find_all_types(type)
    could_use = [Reference(id) for id in ids if id not in already_using]
    already_using = map(Reference, already_using)
    for actor in could_use:
      actor.help_request(already_using)
  
  def name(self, alias, gpid):
    hashes = hash(alias)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    for ahash in hashes:
      manager = network_locator.connect()
      manager.put_gpid_by_name(alias, ahash, gpid)
      manager.disconnect()

  def find_name(self, alias):
    hashes = hash(alias)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    # TODO - Move hashing into manager?
    for ahash in hashes:
      try:
        manager = network_locator.connect()
        gpid = manager.get_gpid_by_name(alias, ahash)
        manager.disconnect()
        return gpid
      except:
        pass
  
  def find_type(self, type):
    hashes = hash(type)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    # TODO - Move hashing into manager?
    for ahash in hashes:
      try:
        manager = network_locator.connect()
        gpid = manager.get_gpid_by_type(type, ahash)
        manager.disconnect()
        return Reference(gpid)
      except:
        pass
        
        
  
  def find_all_types(self, type):
    hashes = hash(type)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    # TODO - Move hashing into manager?
    for ahash in hashes:
      try:
        manager = network_locator.connect()
        gpids = manager.get_gpids_by_type(type, ahash)
        manager.disconnect()
        return gpids
      except:
        pass
  
  def put_type(self, type, gpid, old_gpid = None):
    hashes = hash(type)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    # It's ok to remove actor_id from the type store before
    # adding migration information.
    # [See Appendix D: Inductive Proof on Migration Safeness]
    for ahash in hashes:
      manager = network_locator.connect()
      # This takes care of removing the old gpid- they will
      #  stored at the same node since the type is unchanged
      manager.put_gpid_by_type(type, ahash, gpid, old_gpid)
      manager.disconnect()
    if old_gpid:
      # add migration information
      hashes = hash(old_gpid)
      for ahash in hashes:
        manager = network_locator.connect()
        manager.put_migration(gpid, old_gpid, ahash)
        manager.disconnect()
 
  def get_migration(self, old_gpid):
    #if ids.ip(old_gpid) == ids.ip_from_loc(self.__hostname):
    #  # If it used to be a local actor there's a chance 
    #  #  it has migrated to another core (rather than node)
    #  id_num = ids.num(old_gpid)
    #  port = self.__shared_data.port_from_id(id_num)
    #  if port != 0:
    #    return ids.change_port(old_gpid, port)
      
    hashes = hash(old_gpid)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    # TODO - Move hashing into manager?
    for ahash in hashes:
      try:
        manager = network_locator.connect()
        gpid = manager.get_migration(old_gpid, ahash)
        manager.disconnect()
        return gpid
      except:
        pass
    return None
    
  def import_script(self, module_name):
    # Finds script, stores it locally, returns its local path
    hashes = hash(module_name)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    exists = False
    # Recursive routing only to get script location...
    for ahash in hashes:
      try:
        manager = network_locator.connect()
        (exists, loc) = manager.script_exists(module_name, ahash)
        manager.disconnect()
        break
      except:
        pass
    if not exists:
      return None
    # ...then grab file directly to limit network traffic
    network_locator = rpc.RPCConnector(loc)
    locator = network_locator.connect()
    name = locator.script_store.get_script(module_name, ahash)
    manager.disconnect()
    return name

  def store_script(self, module_name, src):
    # Finds script, stores it locally, returns its local path
    hashes = hash(module_name)
    random.shuffle(hashes)
    network_locator = rpc.RPCConnector(self.__manager_loc)
    exists = False
    for ahash in hashes:
      try:
        # Recursive routing only to get script location...
        manager = network_locator.connect()
        (exists, loc) = manager.script_exists(module_name, ahash)
        manager.disconnect()
        # ...then put file directly (iff it does not exist) to limit network traffic
        if not exists:
          network_locator = rpc.RPCConnector(loc)
          locator = network_locator.connect()
          name = locator.script_store.put_script(module_name, src, ahash)
          manager.disconnect()
      except:
        pass

  def send(self, actor_id, message):
    """Send a message to another actor"""
    return self.__messenger.send(actor_id, message)
    
  def stopping(self, actor):
    """Notifly the theatre that you are intending to die"""
    # TODO: re-implement
    pass
    #self.__reg.unregister(actor)
  
  def migrate_to(self, actor, address):
    """Migrate to a new theatre"""
    return self.__migrator.migrate_to(actor, address)
  
  
  def globally_register_network_actor(self, actor_id, type):
     self.put_type(type, actor_id)
     
  def globally_reregister_network_actor(self, actor_id, type, old_gpid):
     self.put_type(type, actor_id, old_gpid)
    
  def globally_register_named_singleton(self, name, suggested_loc, actor_info):
    hashes = hash(name)
    network_locator = rpc.RPCConnector(self.__manager_loc)

    # Locking is only done at node level so the same node must be tried first
    # by all theaters to allow local locking
    exists = False
    done = False
    while len(hashes) > 0 and not done:
      # Iterate to find the first availible manager that is responisble
      ahash = hashes.pop(0)
      try:
        manager = network_locator.connect()
        (actor_id, exists) = manager.create_named_singleton(name, suggested_loc, actor_info, ahash)
        manager.disconnect()
        done = True
      except:# Exception as inst:
        #print inst
        pass
    if not exists:
        # Has only been registered at first node, need to do the rest
      while len(hashes) > 0:
        ahash = hashes.pop(0)
        try:
          manager = network_locator.connect()
          manager.put_gpid_by_name(name, ahash, actor_id)
          manager.disconnect()
        except:
          pass
    return (actor_id, exists)
  
  def atheatre(self):
    # TODO: work out what, remove?
    """Returns a random theatre in the ActorSpace"""
    return self.__migrator.atheatre()

  def say_hello(self):
	print "Hello"
	
  def get_manager_loc(self):
	return self.__manager_loc