class CallAggregator(object):
  
  def __getattr__(self, name):
    if self.__dict__.has_key(name):
      return self.__dict__[name]
    return Callback(name, self)

  def method_called(self, method, args):
    raise AbstractMethodException()

  
class Callback(object):

  def __init__(self, name, handler):
    self.__name = name
    self.__handler = handler
    
  def __call__(self, *args):
    return self.__handler.method_called(self.__name, args)
  
  
class MethodModifier(object):
  
  def __getattr__(self, name):
    if self.__dict__.has_key(name):
      method = self.__dict__[name]
      if callable(method):
        return self.modified_method(name)
    return object.__getattr__(self, name)
  
  def modified_method(self, name):
    raise AbstractMethodException()
  
class ModifiedMethodCall(object):
  
  def __init__(self, name):
    self.__name = name
    
  def __call__(self, *args):
    return self.modified_method_called(self.__name, args)
  
  def modified_method_called(self, name, args):
    raise AbstractMethodException()  