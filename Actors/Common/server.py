from Actors.keywords import *

class GenericServer(NetworkSingletonActor):

  def theatreclosing(self):
    migrate_or_die()

class BServer(GenericServer):
  """I represent a server actor which maintains a list
     of all the child actors which are to interact with me"""
       
  def birth(self):
    self.children = []
  
  def addchild(self, child):
    if not child in self.children:
      self.children.append(child)
    self.changed()
    
  def removechild(self, child):
    if child in self.children:
      self.children.remove(child)
    self.changed()
    
  def changed(self):
    """Override to add behaviour on a change in the 
       children"""
    pass  
    
  def actorlost(self, actor, message):
    self.removechild(actor)