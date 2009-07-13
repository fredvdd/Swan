from Actors.keywords import *
import random

class RandomGenerator(LocalSingletonActor):
  
  def getrandom(self, lower, upper):
    return random.randint(lower, upper)