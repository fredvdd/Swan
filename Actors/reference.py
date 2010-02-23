from threadlocal import thread_local
from Util.exceptions import AbstractMethodException
from Actors.encapsulatedmethodcall import EncapsulatedMethodCall
from Host.static import log
from Util.Network import rpc

class Reference(object):

  def __getattr__(self, name):
    if self.__dict__.has_key(name):
      return self.__dict__[name]
    return EncapsulatedMethodCall(self.actor_id, name, self)

  def __init__(self, actor_id):
    self.actor_id = actor_id
    
  def __deepcopy__(self, memo):
    return Reference(self.actor_id)  
    
  def __getstate__(self):
    return (self.actor_id,)

  def __setstate__(self, state):
    self.actor_id = state[0]

  def __eq__(self, other):
    if other == None:
      return False
    return self.actor_id == other.actor_id
    
  def __ne__(self, other):
    if other == None:
      return True
    return self.actor_id != other.actor_id  
    
  def __hash__(self):
    return self.actor_id.__hash__()

  def __str__(self):
    return "Actor with id \"%s\"" % self.actor_id

  def __iter__(self):
	res = EncapsulatedMethodCall(self.actor_id, 'iterator', self)()
	return res.__iter__()