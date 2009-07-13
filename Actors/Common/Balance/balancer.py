from Actors.keywords import *
from Actors.Common.server import GenericServer
from Actors.Common.theatre import TheatreList
from Actors.Device.misc import RandomGenerator
import math

class LoadBalancer(GenericServer):
  """I am the external interface to the load balancer"""
  
  def birth(self):
    GenericServer.birth(self)
    # Register to be informed about updates to the
    # theatre list
    TheatreList().register(self.theatres_changed)
    # The strategy specfies how load balancing will
    # proceed.  By default does no balancing.  Use
    # set_strategy to use a more useful strategy
    self.strategy = None
    # The location of each of the actors (as currently known)
    self.locations = ActorLocations()
  
  def set_strategy(self, strategy):
    strategy.set_locations(self.locations)
    self.strategy = strategy
    self.strategy.theatres_changed(TheatreList().theatres())
    
  def friends(self):
    friends = [self.locations] 
    if self.strategy:
      friends.append(self.strategy)
    return friends
    
  def add(self, actor, location):
    self.locations.actor_at(actor, location)

  def update(self, actor, location):
    self.locations.actor_at(actor, location)
    
  def theatres_changed(self):
    self.strategy.theatres_changed(TheatreList().theatres())

class BalancedActor(MobileActor):
  
  def birth(self):
    LoadBalancer().add(self, here())

  def arrived(self):
    LoadBalancer().update(self, here())

class ActorLocations(MobileActor):
  
  def birth(self):
    self.locations = dict()
  
  def actor_at(self, actor, location):
    if not location in self.locations:
      self.locations[location] = [actor,]
    else:
      existing = self.locations[location]
      existing.append(actor)
      
  def whos_at(self, location):
    if not location in self.locations:
      return []
    else:
      return self.locations[location]
    
  def an_actor_from(self, location):
    possible_actors = self.whos_at(location)
    number_on_host = len(possible_actors)
    if number_on_host == 0:
      return None
    index = sync(RandomGenerator().getrandom(0, number_on_host -1))
    return possible_actors[index]