from encapsulatedmethodcall import EncapsulatedMethodCall

class PotentialMethodCall(object):

  def __init__(self, name, handler):
    self.__name = name
    self.__handler = handler
    
  def __call__(self, *args, **kwds):
    return self.__handler.method_called(self.__name, args, kwds)

  def __deepcopy__(self, memo):
    return EncapsulatedMethodCall(self.__handler.result.actor_id, self.__name)

class Result(object):
   
  def __init__(self, actor, result_id):
    self.result_id = result_id
    self.actor = actor
    self.result = None
   
  def __getstate__(self):
    self.__force_result()
    return (self.result,)

  def __setstate__(self, state):
    self.result = state[0]
   
  def __deepcopy__(self, memo):
    self.__force_result()
    return self.result
    
  def method_called(self, name, args, kwds):
    self.__force_result()
    return getattr(self.result, name)(*args, **kwds)
  
  def __iter__(self):
    self.__force_result()
    return self.result.__iter__()
  
  def __getitem__(self, x):
    self.__force_result()
    return self.result[x]
  
  def __add__(self, other):
    self.__force_result()
    return other + self.result 

  def __radd__(self, other):
    self.__force_result()
    return self.result + other
  
  def __mul__(self, other):
    self.__force_result()
    return other * self.result 

  def __rmul__(self, other):
    self.__force_result()
    return self.result * other
  
  def __div__(self, other):
    self.__force_result()
    return self.result.__div__(other)

  def __rdiv__(self, other):
    self.__force_result()
    return self.result.__rdiv__(other)
  

  def __int__(self):
     self.__force_result()
     return int(self.result)
  
  def __long__(self):
     self.__force_result()
     return long(self.result)
  
  def __float__(self):
     self.__force_result()
     return float(self.result)
    
  def __not__(self):
    self.__force_result()
    return not self.result  
  
  def __str__(self):
    self.__force_result()
    return self.result.__str__()
  
  def __len__(self):
    self.__force_result()
    return self.result.__len__()
   
  def __eq__(self, other):
    self.__force_result()
    return self.result == other
   
  def __getattribute__(self, name):
    try:
      return object.__getattribute__(self, name)
    except AttributeError:
      return PotentialMethodCall(name, self)
  
  def __force_result(self):
     if not self.result:
       self.result = self.actor.result(self.result_id)