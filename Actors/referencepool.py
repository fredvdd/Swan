from threadlocal import thread_local
from Util.exceptions import AbstractMethodException
from Actors.encapsulatedpoolcall import EncapsulatedPoolCall, EncapsulatedRepeatedPoolCall
from Actors.reference import Reference
from Host.static import log
from threading import Timer
from itertools import cycle

class ReferencePool(object):

  def __getattr__(self, name):
    if self.__dict__.has_key(name):
      return self.__dict__[name]
    return EncapsulatedPoolCall(self.actor_ids, name, self)

  def __init__(self, actor_ids):
    self.actors = cycle([Reference(id) for id in actor_ids])
    self.actor_ids = actor_ids
    
  def __deepcopy__(self, memo):
    return ReferencePool(self.actor_ids)  
    
  def __getstate__(self):
    return (self.actor_ids,)

  def __setstate__(self, state):
    self.actor_ids = state[0]
    
  # def __hash__(self):
  #   return self.actor_id.__hash__()

  def __str__(self):
    str = "Actor with ids: "
    for actor_id in self.actor_ids:
      str = str + actor_id + " "
    return str

  def one(self):
    return self.actors.next()

  def all(self):
    return RepeatedReferencePool(self.actor_ids)
	
class RepeatedReferencePool(ReferencePool):
  
  def __getattr__(self, name):
    if self.__dict__.has_key(name):
      return self.__dict__[name]
    return EncapsulatedRepeatedPoolCall(self.actor_ids, name)
	