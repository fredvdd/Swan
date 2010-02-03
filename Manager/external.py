import threading
import random
from managerlog import log
from overlay import Overlay
from portstore import SocketStore
from Util.Network import socketutil

class ManagerExternalInterface(object):
  
  def __init__(self, overlay, name_store, type_store, migration_store, script_store):
    self.__locations = dict()
    self.__overlay = overlay
    self.__name_store = name_store
    self.__type_store = type_store
    self.__migration_store = migration_store
    self.__script_store = script_store
    self.__location_lock = threading.Lock()
    self.__theatre_lock = threading.Lock()
    self.__theatres = []
    self.__socket_store = SocketStore(overlay)
    log.debug(self, 'initialised')

  def addnode(self, id, location):
    #self.__theatre_lock.acquire()
    self.__overlay.add(id, location)
    #self.here
    #self.__overlay.addAll(nodes)
    #self.__theatre_lock.release()
    
    
  def sendreq(self):
    return self.__overlay.get_all()
    
  def get_gpid_by_name(self, alias, hash):
    return self.__name_store.get(alias, hash)

  def put_gpid_by_name(self, alias, hash, gpid):
    self.__name_store.put(alias, gpid, hash)
  
    
  def get_gpids_by_type(self, type, hash):
    return self.__type_store.get_all(type, hash)

  def get_gpid_by_type(self, type, hash):
    return self.__type_store.get(type, hash)      
    
  def put_gpid_by_type(self, type, hash, gpid, old_gpid = None):
    self.__type_store.put(type, gpid, hash, old_gpid)

  def get_migration(self, old_gpid, hash):
    return self.__migration_store.get(old_gpid, hash)

  def put_migration(self, gpid, old_gpid, hash):
    self.__migration_store.put(gpid, old_gpid, hash)
         
  def create_named_singleton(self, name, suggested_loc, actor_info, hash):
    return self.__name_store.create_named_singleton(name, suggested_loc, actor_info, hash)

  def get_script(self, module_name, hash):
    src = self.__script_store.get(module_name, hash)
    return self.__script_store.put_script(module_name, src, hash)
  
  def put_script(self, module_name, src, hash):
    self.__script_store.put(module_name, src, hash)
    
  def put_script_locally(self, module_name, src):
    return self.__script_store.put_locally(module_name)  

  def script_exists(self, module_name, hash):
    return self.__script_store.exists(module_name, hash)
    
    
  
  def theatrestarted(self, theatre):
    self.__theatre_lock.acquire()
    self.__theatres.append(theatre)
    self.__theatre_lock.release()
    
  def theatreterminated(self, theatre):
    self.__theatre_lock.acquire()
    if theatre in self.__theatres:
      self.__theatres.remove(theatre)
    self.__theatre_lock.release()

  def atheatre(self, excluding):
    self.__theatre_lock.acquire()
    num = len(self.__theatres)
    if num == 0 or (num == 1 and self.__theatres[0] == excluding):
      result = None 
    else:
      result = excluding
      while result == excluding:
        rindex = random.randint(0, len(self.__theatres) -1)
        result = self.__theatres[rindex]
    self.__theatre_lock.release()
    return result

  def whereis(self, actor_id):
    log.debug(self, 'whereis actor with id = %s' % actor_id)
    self.__location_lock.acquire()
    location = None
    if self.__locations.has_key(actor_id):
      location = self.__locations[actor_id]
      log.debug(self, 'FOUND - actor with id = %s at %s' % (actor_id, location))
    else:
       log.debug(self, 'NOT FOUND - location of actor with id = %s not known' % actor_id)
    self.__location_lock.release()
    return location
   
  def globalactoris(self, actor_id, location):
    self.__location_lock.acquire()
    log.debug(self, 'globalactoris request, actor with id = %s at location %s' % (actor_id, location))
    existing_location = None
    if self.__locations.has_key(actor_id):
      existing_location = self.__locations[actor_id]
      log.debug(self, 'global actor ALREADY registered. Id = %s already at location %s' % (actor_id, existing_location))
    else:
      self.__locations[actor_id] = location
      log.debug(self, 'global actor registered. Id = %s registered at location %s' % (actor_id, location))
    self.__location_lock.release()
    return existing_location
  
  def actoris(self, actor_id, location):
    self.__location_lock.acquire()
    log.debug(self, 'actoris request, actor with id = %s at location %s' % (actor_id, location))
    location = self.__locations[actor_id] = location 
    log.debug(self, 'actor registered. Id = %s registered at location %s' % (actor_id, location))
    self.__location_lock.release()

  def isdead(self, actor_id):
    self.__location_lock.acquire()
    log.debug(self, 'isdead request - actor with id = %s' % actor_id)
    if self.__locations.has_key(actor_id):
      del self.__locations[actor_id]
      log.debug(self, 'REMOVE - actor removed. id = %s' % actor_id)
    else:
      log.debug(self, 'death attempted on non-existant actor. Id = %s' % actor_id)
    self.__location_lock.release()

  def isrunning(self):
    """Dummy method to allow theatres to check initial
       connectivity"""
    return True

  def __str__(self):
    return 'ManagerExternalInterface'

  def open_socket(self, port):
    log.debug(self, "Opening port %d" % port)
    return self.__socket_store.open_socket(port)

  def connect_socket(self, address):
	log.debug(self, "Connecting to %s:%d" % address)
	return self.__socket_store.connect_socket(address)
	
  def close_socket(self, socket):
	log.debug(self,"Closing socket %s" % socket)
	self.__socket_store.get_socket(socket).close()
	
  def socket_call(self, socket, method, *args, **kwds):
    log.debug(self,"Call %s on socket %s with args %s " % (method, socket, args))
    return getattr(self.__socket_store.get_socket(socket), method)(*args, **kwds)
    #return "Goodbye"