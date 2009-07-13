class Shared(object):

  def __init__(self, port, current_id, id_lock, core_store, store_lock, current_creator, creator_lock, port_range):
    self.port = port
    self.current_id = 0
    self.id_lock = id_lock
    self.core_store = core_store
    self.store_lock = store_lock
    self.current_creator = current_creator
    self.creator_lock = creator_lock
    self.port_range = port_range
  
  def next_id_num(self):
    id_num = self.current_id
    self.current_id += 1
    return id_num
    
  def next_port(self):
    return self.port
    
  def id_at_port(self, id_num):
    pass
    
  def port_from_id(self, id_num):
    #self.store_lock.acquire()
    port = self.core_store[id_num]
    #self.store_lock.release()
    return 0