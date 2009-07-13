class Shared(object):

  def __init__(self, port, current_id, id_lock, core_store, store_lock, current_creator, creator_lock, port_range):
    self.port = port
    self.current_id = current_id
    self.id_lock = id_lock
    self.core_store = core_store
    self.store_lock = store_lock
    self.current_creator = current_creator
    self.creator_lock = creator_lock
    self.port_range = port_range
  
  def next_id_num(self):
    self.id_lock.acquire()
    id_num = self.current_id.value
    self.current_id.value += 1
    self.id_lock.release()
    return id_num
    
  def next_port(self):
    self.creator_lock.acquire()
    port_index = self.current_creator.value
    self.current_creator.value = (port_index + 1) % len(self.port_range)
    self.creator_lock.release()
    return self.port_range[port_index]
    
  def id_at_port(self, id_num):
    self.store_lock.acquire()
    self.core_store[id_num] = self.port
    self.store_lock.release()
    
  def port_from_id(self, id_num):
    #self.store_lock.acquire()
    port = self.core_store[id_num]
    #self.store_lock.release()
    return port