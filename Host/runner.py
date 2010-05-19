import theatre
from Util import signalutil
import settings
from static import log, set_local_theatre
from Util.exceptions import UncontactableLocatorException

class TheatreRunner(signalutil.NewRunner):
  def __init__(self, f, *args, **kwds):
    self.__f = f
    self.__args = args
    self.__kwds = kwds
    
  def begin(self):
    multicore = False
    try:
      import multiprocessing as mp
      from multiprocessing.sharedctypes import Value, Array
      import ctypes
      if mp.cpu_count() > 1:
        multicore = True
    except ImportError: 
        pass
      
    if multicore:  
      self.processes = list()
      cores = mp.cpu_count()
      port_range = range(settings.local_port, settings.local_port + cores)

      actor_store = Array(ctypes.c_short, cores * 2048)
      store_lock = mp.Lock()
      current_id = Value(ctypes.c_int, 0)
      id_lock = mp.Lock()
      current_creator = Value(ctypes.c_int, 0)
      creator_lock = mp.Lock()

      for port in port_range:
        if port != settings.local_port:
          loc = "%s:%s" % (settings.local_name, port)  
          p = mp.Process(target=theatre.Theatre, args=(loc, settings.network_locator_socket, 
            actor_store, store_lock, current_id, id_lock, current_creator, creator_lock, port_range))
          p.start()
          self.processes.append(p)

      # This very process becomes a theatre too
      loc = "%s:%s" % (settings.local_name, settings.local_port)   
      self.theatre = theatre.Theatre(loc, settings.network_locator_socket, 
        actor_store, store_lock, current_id, id_lock, current_creator, creator_lock, port_range, self.__f, self.__args, self.__kwds, self.processes)
   
    else:
      # We can't take advantage of multicore (older python) or don't want to (only one core)
      port_range = [settings.local_port]

      loc = "%s:%s" % (settings.local_name, settings.local_port)   
      self.theatre = theatre.Theatre(loc, settings.network_locator_socket, 
        None, None, None, None, None, None, port_range, self.__f, [])

   
  def __str__(self):
    return 'TheatreRunner'

  
def initialise(f, *args, **kwds):
  TheatreRunner(f, *args, **kwds).start()
  
