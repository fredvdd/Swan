import threading
from Messaging.message import *
from Host.static import log
from Util.exceptions import MethodNotSupportedException
from threadlocal import thread_local
import traceback

class ActorRunner(threading.Thread):
  """I run an actor""" 
  
  def __init__(self, actor):
    threading.Thread.__init__(self)
    self.__actor = actor
    self.__death_signal = False
   
  def stop(self):
     self.__death_signal = True
    
  def run(self):
    thread_local.actor = self.__actor
    while(True):
      if self.__death_signal == True:
        return
      m = self.__actor.state.messages.get_next_request()
      if type(m) == RequestMessage:
        self.__process_request(m)
      if type(m) == CallbackMessage:
        self.__process_callback(m)
      if type(m) == ActorJoinMessage:
        self.__process_actor_join(m)
      if type(m) == SpecialMessage:
        self.__process_special(m)

  
  def __process_request(self, request):
    log.debug(self, 'processing: ' + str(request))
    method = self.__actor.state.get_method(request.name)
    try:
      result = self.__callmethod(method, request.args, request.kwds)
    except Exception:
      return
    if request.origin:
      reply = ResponseMessage(request.id, result)
      self.__actor.theatre.send(request.origin, reply)

  def __process_callback(self, callback):
    method = self.__actor.state.get_method(callback.name)
    args = [callback.result]
    args.extend(callback.args)
    self.__callmethod(method, args, callback.kwds)
    
  def __process_actor_join(self, actor_join):
    method = self.__actor.state.get_method(actor_join.name)
    try:
      self.__callmethod(method, actor_join.data, dict())
    except Exception:
      return
    
  def __process_special(self, special):
    method = self.__actor.state.get_method(special.name)
    try:
      self.__callmethod(method, special.data, special.kwds)
    except Exception:
      pass
    if special.name == 'theatreclosing':
      self.__actor.die()
    
  def __callmethod(self, method, args, kwds):
    try:
      return method(*args, **kwds)
    except Exception, e:
      print e
      print traceback.format_exc()
      self.__actor.state.joinactor('error',  [e])
      raise e
      
  def __str__(self):
    return 'ActorRunner for %s' % self.__actor