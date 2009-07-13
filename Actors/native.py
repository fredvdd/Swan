from Host.static import local_theatre
from Messaging.message import RequestMessage
from Actors.keywords import *

def send(actor_ref, name, *args, **kwds):
  actor_id = actor_ref
  if hasattr(actor_ref, 'actor_id'):
    actor_id = actor_ref.actor_id
  message = RequestMessage(0, name, args, kwds)
  return local_theatre().send(actor_id, message)

""""#def send_recieve(actor_ref, name, *args):
#  probe = NativeProbe(actor_ref, name, args)
#  
#class NativeProbe(LocalActor):
#  
#  def birth(self, target, method, args):
#    sync(target.method(*args))"""