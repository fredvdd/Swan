import threading
import Util.ids as ids
from collections import defaultdict

class LocalActorStore(object):
  
  def __init__(self, here, shared_data):
    self.actor_store = dict()
    self.here = here
    self.shared_data = shared_data
    self.types = defaultdict(set)
  
  def add_network_actor(self, ref, actor_id):
    # Type not currently put into actor_id
    self.actor_store[actor_id] = ref
    id_num = ids.num(actor_id)
    self.shared_data.id_at_port(id_num)
    type = ids.type(actor_id)
    self.types[type].add(actor_id)
  
  def get_type(self, type):
    # Only makes sense for static actors? (only ever 1 in this case)
    actor_id = None
    if type in self.types:
      actor_id = list(self.types[type])[0]
    return actor_id
    
  def get_types(self, type):
    # Could be useful if actors encapsulate a device
    actor_ids = list()
    if type in self.types:
      actor_ids = list(self.types[type])
    return actor_ids
  
  def get_ref(self, actor_id):
    # exception for not exists 
    ref = None
    if actor_id in self.actor_store:
      ref = self.actor_store[actor_id]
    return ref

  def get_port(self, actor_id):
    # exception for not exists 
    id_num = ids.num(actor_id)
    return self.shared_data.port_from_id(id_num)

  def remove(self, actor_id):
    # exception for not exists 
    if actor_id in self.actor_store:
      del self.actor_store[actor_id]
      type = ids.type(actor_id)
      if len(self.types[type]) == 1:
        del self.types[type]
      else:
        self.types[type] = self.types[type].discard(loc)  


  def migrating(self, actor):
    #TODO: never used, remove?
    actor_id = actor.state.actor_id
    self.remove(actor_id)
