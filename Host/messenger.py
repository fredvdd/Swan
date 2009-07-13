from Util.Network import rpc
from Util.exceptions import ActorNotFoundException
import copy
from static import log, local_theatre
import time
import Util.ids as ids

MAX_RETRIES = 10

class Messenger(object):
  
  def __init__(self, here, actor_store):
    self.here = here
    self.__actor_store = actor_store
    
  
  def incoming_external(self, actor_id, message):
    return self.message_local(actor_id, message)
  
  def send(self, actor_id, msg):
     message = copy.deepcopy(msg)
     success = False
     retries = 0
     new_actor_id = None
     actor_location = ids.loc(actor_id)
     while not success and retries < MAX_RETRIES:
       conn = rpc.RPCConnector(actor_location)
       try:
         if actor_location == self.here:
           (success, new_actor_id) = self.message_local(actor_id, message)
           if success:
             return (True, new_actor_id)
         remote_theatre = conn.connect()
         (success, new_actor_id) = remote_theatre.incoming_message(actor_id, message)
         remote_theatre.disconnect()
         if success:
           return (True, new_actor_id)
         time.sleep(0.8)
       except Exception:
         print 'Senderror:'
         log.warn(self, 'sending message to %s failed, retrying, as host (%s) was unreachable (message was: %s)' % (actor_id, actor_location, message))
         new_actor_id = local_theatre().get_migration(actor_id)
         if new_actor_id:
           actor_id = new_actor_id
           actor_location = ids.loc(actor_id)
         retries += 1 
         continue
       if not success:
         log.warn(self, 'sending message to %s failed retrying (message was: %s)' % (actor_id, message))
         new_actor_id = local_theatre().get_migration(actor_id)
         if new_actor_id:
           actor_id = new_actor_id
           actor_location = ids.loc(actor_id)
         retries += 1 
     log.error(self, 'sending message to %s aborted after %s retries (message was: %s)' % (actor_id, MAX_RETRIES, message)) 
     return (False, new_actor_id)
    
  def message_local(self, actor_id, message):
   """Send a message to a local actor. Returns True iff
      the send was sucessful""" 
   local_actor = self.__actor_store.get_ref(actor_id) 
   if local_actor:
     local_actor.add_message(message)
     return (True, None)
   local_port = self.__actor_store.get_port(actor_id) 
   if local_port:
    actor_id = ids.change_port(actor_id, local_port)
    conn = rpc.RPCConnector(ids.loc(actor_id))
    remote_theatre = conn.connect()
    success = remote_theatre.incoming_message(actor_id, message)
    remote_theatre.disconnect()
    return(success, actor_id)
   return (False, None)
