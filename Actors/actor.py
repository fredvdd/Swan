from runner import ActorRunner
from Host.static import log
from encapsulatedmethodcall import EncapsulatedMethodCall
from Messaging.message import RequestMessage
from reference import Reference
from referencepool import ReferencePool
import inspect
import threading
from result import Result

class Actor(object):
  """I represent the logical concept of an actor.  I encapsulate
     both the state and the thread of execution of an actor."""
   
  def __init__(self, theatre):
    self.theatre = theatre
    self.state = None
    self.ready = threading.Condition()
    
  def getmodule(self):
    """Returns the module in which the actor is defined"""
    return inspect.getmodule(self.state)  
    
  def setstate(self, state):
    self.ready.acquire()
    self.state = state
    # Notify any actors waiting for this actor to be
    # initialised, prevents racing for singleton creation
    self.ready.notifyAll()
    self.ready.release()
    
  def add_message(self, message):
   """Entry point for external (message) interaction with 
      an actor and is thread safe."""
   self.ready.acquire()
   while not self.state:
     self.ready.wait()
   self.ready.release()
   log.debug(self.state, "received message - %s" % message)
   self.state.messages.add(message)

  def start(self):
    """Begins the execution of the actor"""
    runner = ActorRunner(self)
    self.__runner = runner
    runner.start()
    
  def stop(self):
    self.__runner.stop()
  
  def result(self, request_id):
    return self.state.messages.wait_for_result(request_id)

  def has_result(self, request_id):
    return self.state.messages.has_result(request_id)

  def add_callback(self, method, request_id):
    message = self.state.messages.add_callback(method, request_id)      
  
  
  def die(self):
    """Kills the actor"""
    # Inform the local theatre that we are an actor down
    self.theatre.stopping(self)
    self.__runner.stop()

  def name(self, alias, actor_ref):
    if actor_ref is None:
      actor_id = self.state.actor_id
    else:
      actor_id = actor_ref.actor_id
    print "naming " + actor_id + " " + alias
    self.theatre.name(alias, actor_id)
  
  def find_name(self, alias):
    return self.theatre.find_name(alias)

  def find_type(self, type):
    print "finding type " + type
    return self.theatre.find_type(type)

  def find_all_types(self, type):
    print "finding all types " + type
    actor_ids = self.theatre.find_all_types(type)
    return map(Reference, actor_ids)
    
  def get_pool(self, cls, *args, **kwds):
    print "getting pool " + cls.__name__
    return self.theatre.get_pool(cls, *args, **kwds)

  
  def migrate_to(self, address):
    # The actor cannot perform the migration itself since
    # there are a number of locking an consistency issues - 
    # delegate the migration to 
    self.theatre.migrate_to(self, address)
    
  #def get_encapsulated_method(self, method):
   #  return  (self.state.actor_id, method)
   
  def sendmessage(self, to, name, args, kwds):
    # Generate a new unique ID for the message
    id = self.state.messages.new_request()
    message = RequestMessage(id, name, args, kwds)
    # Add ourselfves as the origin such that we are
    # notified when the message has been processed
    message.add_origin(self.state.actor_id)
    # Attempt to send the message
    (success, new_actor_id) = self.theatre.send(to, message)
    if not success:
      log.debug(self, "cannot find actor with id %s" % to)
      self.state.joinactor('actorlost',  [Reference(to), message])
    return (Result(self, id), new_actor_id)
  
  def __str__(self):
    # Delegate the description to the state
    return str(self.state)   
