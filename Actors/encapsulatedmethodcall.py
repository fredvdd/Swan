from threadlocal import thread_local
from Actors.native import send

class EncapsulatedMethodCall(object):
  
  def __init__(self, source, method, ref_to_ref):
    self.__source = source
    self.__method = method
    self.__ref_to_ref = ref_to_ref
  
  def __call__(self, *args, **kwds):
    if hasattr(thread_local, 'actor'):
      actor = thread_local.actor
      if actor.state.actor_id == self.__source:
        return actor.state.get_method(self.__method)(*args, **kwds)
      else:
        (val, actor_id) = actor.sendmessage(self.__source, self.__method, args, kwds)
        if actor_id:
          self.__ref_to_ref.actor_id = actor_id
        return val
    else:
      return send(self.__source, self.__method, *args, **kwds)
