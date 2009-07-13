from Actors.keywords import *

class SimpleSingleton(NamedSingletonActor):

  def birth(self):
    print("Created")
    
  def hi(self):
    return "hello"