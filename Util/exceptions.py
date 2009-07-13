class AbstractMethodException(Exception):

  def __init__(self):
    Exception.__init__(super, "Abstract method must be overridden")
    
class MethodNotSupportedException(Exception):
  def __init__(self, actor, method):
    Exception.__init__(self, "Actor type '%s' does not support method '%s'" % (actor.__class__.__name__, method))

class ActorNotFoundException(Exception):
  def __init__(self, actor_id):
    Exception.__init__(self, 'Actor with ID %s could not be found' % actor_id)
    
class UncontactableLocatorException(Exception):
    def __init__(self, address):
      Exception.__init__(self, 'Network locator (%s) could not be contacted' % address)
      
class ActorsOfTypeNotFoundException(Exception):
    def __init__(self, address):
      Exception.__init__(self, 'No actors of type (%s) exist and they are not allowed to be created automatically' % type)