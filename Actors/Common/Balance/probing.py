from Actors.keywords import *
from Actors.Device.status import TheatreStatus
from Actors.Device.timer import SyncTimer, Clock
from Actors.Device.misc import RandomGenerator

# REPRESENTS THE LOAD OF A THEATRE
UNDERLOADED = 0
JUST_RIGHT = 1
OVERLOADED = 2

class ProbingStrategy(MobileActor):
  """I am a load balancing strategy which
     maps actors to hosts by sending probes to 
     theatres."""
     
  def birth(self):
    self.statuses = dict()
     
  def set_locations(self, locations):
    self.locations = locations
     
  def theatres_changed(self, theatres):
    for theatre in theatres:
      if not theatre in self.statuses:
        LoadProbe(theatre, self.report)
        self.statuses[theatre] = JUST_RIGHT # Until futher knowledge
    for key in self.statuses.keys():
      if not key in theatres:
        del self.statuses[key]
        
  def report(self, host, load):
    """Called by a probe when the state of its host
       has changed"""
    self.statuses[host] = load
    self.rebalance()
    
  def rebalance(self):
    bad_host = self.an_overloaded_host()
    if bad_host == None:
      return
    
    an_actor = self.locations.an_actor_from(bad_host)
   
    if an_actor == None:
      return
    good_host = self.an_underloaded_host()
    
    if good_host == None:
      return

    an_actor.migrate_to(good_host)
    return
    
  def an_overloaded_host(self):
    """ Returns an overloaded host"""
    overloaded = []
    for (theatre, status) in self.statuses.items():
      if status == OVERLOADED:
        overloaded.append(theatre)
    return random_elem(overloaded)
      
  def an_underloaded_host(self):
    underloaded = []
    """ Returns an overloaded host"""
    for (theatre, status) in self.statuses.items():
      if status == UNDERLOADED:
        underloaded.append(theatre)
    return random_elem(underloaded)

def random_elem(list):
  size = len(list)
  if size == 0:
    return None
  index = sync(RandomGenerator().getrandom(0, size-1))
  return list[index]

class LoadProbe(MobileActor):
  """I am a load probe which reports load changes"""
  def birth(self, target_host, report):
    self.report = report
    self.status = JUST_RIGHT 
    migrate_to(target_host)

  def arrived(self):
    SyncTimer(self.check_status, 2)
   
  def check_status(self):
    load = TheatreStatus().loadaverage()[0]
    time = Clock().time_in_seconds()
    print '%s\t\t%s' % (time, load)
    if load < 0.6:
      new_status = UNDERLOADED
    elif load < 0.8:
      new_status = JUST_RIGHT
    else:
      new_status = OVERLOADED 
      self.status = OVERLOADED
      self.phone_home()
      return
    if new_status != self.status:
      self.status = new_status
      self.phone_home()
      
  def phone_home(self):
    self.report(here(), self.status) 