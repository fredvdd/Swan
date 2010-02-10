from threadlocal import thread_local
from actorstate import ActorState
from actor import Actor
from Host import runner
from Host.static import local_theatre
from Actors.reference import Reference
import types
from result import Result
import inspect
from Util.Network import rpc
from Util import picklecode
import pickle
import Util.ids as ids

def migrate_to(remote_theatre):
  actor = thread_local.actor
  friends = actor.state.friends()
  for friend in friends:
    friend.migrate_to(remote_theatre)
  actor.migrate_to(remote_theatre)

class LocalSingletonActor(ActorState):
  def __new__(cls, *args, **kwds):
    actor = Actor(local_theatre())
    type = cls.__name__
    (actor_id, exists) = actor.theatre.globally_register_local_singleton(actor, type)
    if not exists:
      actorstate = object.__new__(cls)
      actorstate.__init__(type, actor_id)
      actorstate.singleton = True
      actorstate.add_birth(args, kwds)
      actor.setstate(actorstate)
      actor.start()
    return Reference(actor_id)
    
class NetworkSingletonActor(ActorState):
  def __new__(cls, *args, **kwds):
    actor = Actor(local_theatre())
    type = cls.__name__
    (actor_id, exists) = actor.theatre.globally_register_global_singleton(actor, type)
    if not exists:
      actorstate = object.__new__(cls)
      actorstate.__init__(type, type)
      actorstate.singleton = True
      actorstate.add_birth(args, kwds)
      actor.setstate(actorstate)
      actor.start()
    return Reference(actor_id)
    

class NamedSingletonActor(ActorState):
  def __new__(cls, *args, **kwds):
    actor = Actor(local_theatre())
    type = cls.__name__
    module_name = inspect.getmodule(cls).__name__
    name = type + '-'
    if len(args) > 0:
      args_list = list(args)
      name = args_list.pop(0)
      args = tuple(args_list)
    suggested_loc = local_theatre().where_to_create()
    (actor_id, exists) = actor.theatre.globally_register_named_singleton(name, suggested_loc, (cls, module_name, type, args, kwds))
    return Reference(actor_id)
    
class NetworkActor(ActorState):  
  def __new__(cls, *args, **kwds):
    type = cls.__name__
    module_name = inspect.getmodule(cls).__name__
    core_loc = local_theatre().where_to_create()
    if core_loc == local_theatre().gethostname():
       actor_id = local_theatre().create_actor(cls, module_name, type, args, kwds)
    else:
      network_locator = rpc.RPCConnector(core_loc)
      core = network_locator.connect()
      actor_id = core.create_actor(cls, module_name, type, args, kwds)
      core.disconnect()
    return Reference(actor_id)
  
  def migrate_to(self, theatre):
    return migrate_to(theatre)

  def update_method(self, name, code):
    old_func = object.__getattribute__(self, name)
    globals = old_func.func_globals
    function = types.FunctionType(code, globals)
    self.__dict__[name] = types.MethodType(function, self)
    

class LocalActor(NetworkActor):
  def __init__(self, *args):
    NetworkActor.__init__(self, *args)
    
class MobileActor(NetworkActor):
  def __init__(self, *args):
    NetworkActor.__init__(self, *args)
    
class StaticActor(NetworkActor):
  static = True
  def __init__(self, *args):
    NetworkActor.__init__(self, *args)
  

def callback(meth, result):
  thread_local.actor.add_callback(meth, result.result_id)

def ready(result):
  return thread_local.actor.has_result(result.result_id)
  
def local(actor_id):
  return Reference("%s-%s" % (actor_id , local_theatre().gethostname()))

def glob(actor_id):
  return Reference(actor_id)

def name(alias, actor_ref = None):
  thread_local.actor.name(alias, actor_ref)
  
def find_name(alias):
  actor_id = thread_local.actor.find_name(alias)
  return Reference(actor_id)

def find_type(type):
  return thread_local.actor.find_type(type)

def find_all_types(type):
  return thread_local.actor.find_all_types(type)
  
def get_pool(type, *args, **kwds):
  return thread_local.actor.get_pool(type, *args, **kwds)

def one(pool):
  return pool.one()

def all(pool):
  return pool.all()  

def update_method(actor, method_ref):
  name = method_ref.func_name
  code = method_ref.func_code
  actor.update_method(name, code)
  
  

def here():
  return local_theatre().gethostname()
  
def die():
  thread_local.actor.die()

def schedule(method):
  return thread_local.actor.state.joinactor(method, [])  

def sync(*requests):
  actor = thread_local.actor
  if (len(requests) > 1):
    return multi_sync(actor, requests)
  if type(requests[0]) == Result:
    return single_sync(actor, requests[0])
  return multi_sync(actor, requests[0])

def single_sync(actor, request):
  return actor.result(request.result_id)

def multi_sync(actor, requests):
  results = []
  for request in requests:
     results.append(actor.result(request.result_id))
  return results

def migrate_or_die():
  atheatre = local_theatre().atheatre()
  if atheatre:
    migrate_to(atheatre)
  
def initialise(f):
  runner.initialise(f)


def open_socket(port):
	manager_loc = local_theatre().get_manager_loc()
	network_locator = rpc.RPCConnector(manager_loc)
	manager = network_locator.connect()
	return manager.open_socket(port)
		#return SocketReference(manager_loc, port)

def connect_socket(address):
	manager_loc = local_theatre().get_manager_loc()
	network_locator = rpc.RPCConnector(manager_loc)
	manager = network_locator.connect()
	return manager.connect_socket(address)