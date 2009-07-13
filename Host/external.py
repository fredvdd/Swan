from Host.static import local_theatre
import pickle

class TheatreExternalInterface(object):
  
  def __init__(self, messenger, migrator, terminal, theatre, actor_store):
    self.__messenger = messenger
    self.__migrator = migrator
    self.__terminal = terminal
    self.__theatre = theatre
    self.__actor_store = actor_store
    
  
  def incoming_message(self, actor_id, message):
    return self.__messenger.incoming_external(actor_id, message)
  
  def get_script(self, modulename):
    self.__migrator.get_script(modulename)
    
  def incoming_actor(self, actor):
    self.__migrator.incoming_actor(actor)
    
  def says(self, sender, msg):
    terminal.queue.put(sender, msg)
    
  def create_actor(self, cls, module_name, type, args, kwds):
    return local_theatre().create_actor(cls, module_name, type, args, kwds)
    
  def get_types(self, type):
    return self.__actor_store.get_types(type)
    
  def shutdown(self):
     self.__theatre.valve.shutdown()
  


