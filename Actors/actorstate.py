from messagestore import MessageStore
from reference import Reference
from Messaging.message import ActorJoinMessage
from Util.exceptions import MethodNotSupportedException
from Actors.encapsulatedmethodcall import EncapsulatedMethodCall
import Util.load as load
import random
import copy
import types

class ActorState(object):
  """I represent the state of an actor which is _not_
     theatre specific"""
  
  static = False
  
  def __init__(self, actortype, actor_id, name = None):
    self.actor_id = actor_id
    self.names = list()
    if name:
      self.names.append(name)
    self.actortype = actortype
    self.messages = MessageStore()
    
  def birth(self):
    """This method should be overridden to specify the actor's initial
       behaviour.  The behaviour may be any (valid) actor interaction"""
    pass
  
  def theatreclosing(self):
    """This method should be overridden to specify the actor's 
        behaviour upon termination of its current theatre.  Note an actor's collaborators may also be
        terminating thus only migration or singleton interaction should be perfomed"""
    pass

  def arrived(self):
    """This method is called when an actor arrives at its destination host"""
    pass
  
  def actorlost(self, actor, message):
    """This method is called when sending to an actor fails"""
    pass
  
  def error(self, e):
    """Called when an error occurs"""
    print e
  
  def friends(self):
    return []
  
  def __getattribute__(self, name):
    if name.startswith("__") or name.startswith("ext_") or name in ["methods", "get_method", "add_birth", "add_arrived", "add_closing", "joinactor", "actor_id", "actortype", "messages"]:
      return object.__getattribute__(self, name)
    else:
      attr =  object.__getattribute__(self, name)
      if isinstance(attr, types.MethodType):
        return EncapsulatedMethodCall(self.actor_id, name, self)   
      return attr
  
  def __eq__(self, other):
    return self.actor_id == other.actor_id
  
  def __ne__(self, other):
     return self.actor_id != other.actor_id  
  
  def __str__(self):
    return "Actor(\"%s\")" % (self.actor_id)
   
  def __deepcopy__(self, memo):
    return Reference(self.actor_id)

  def __getstate__(self):
    return self.__dict__

  def __setstate__(self, state):
    self.__dict__ = state

  def get_method(self, name):
    method = object.__getattribute__(self, name)
    if not callable(method):
      raise MethodNotSupportedException(self, name)
    return method
  
  def add_birth(self, args, kwds):
    copiedargs = copy.deepcopy(args)
    copiedkwds = copy.deepcopy(kwds)
    self.messages.add_front('birth', copiedargs, copiedkwds)
  
  def add_arrived(self):
    self.messages.add_front('arrived', [], dict())
  
  def add_closing(self):
    self.messages.addfront('theatreclosing', [], dict())
  
  def joinactor(self, method, args):
    self.messages.add(ActorJoinMessage(method, args))
    
  def help_request(self, actors):
    print 'help req rec'
    queue_length = len(self.messages)
    if queue_length <= 10 and load.is_underloaded():
      helper = Reference(self.actor_id)
      for actor in actors:
        actor.help_offer(helper, queue_length, len(actors))

  def help_offer(self, helper, helper_queue_length, num_to_share_with):
    # The num_to_share_with is the number of actors that you
    # are sharing this request with- to play nice you should
    # send this factor less of the load we were going to send.
    # It's as if there's a chocolate cake...
    
    queue_length = len(self.messages)
    if self.messages.split == 0:
      self.messages.split = float(queue_length) / (float(self.messages.offers) + float(num_to_share_with))
    split = self.messages.split
    to_send = int(split)
    if random.uniform(0,1) < (split % 1):
      to_send += 1
    if self.messages.offers == 1:
      self.messages.split = 0
    print "split is:" + str(to_send) + " off is:" + str(self.messages.offers)
    start = queue_length - to_send
    messages = self.messages.get_messages(start, queue_length)
    if len(messages) > 0:
      helper.add_all(messages)
    self.messages.offers -= 1
