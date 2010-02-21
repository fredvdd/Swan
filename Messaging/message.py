# I am the object generated when an actor wishes to invoke
# a method on another actor.
# The message returned in response should identify itself as
# such by including the 'id' in the reponse message.
class RequestMessage(object):
  
  def __init__(self, id, name, args, kwds):
    self.name = name
    self.args = args
    self.kwds = kwds
    self.id = id
    self.origin = None

  def add_origin(self, origin):
    self.origin = origin

  def __str__(self):
    return 'RequestMessage (id = %s), name: %s args: %s' % (self.id, self.name, self.args)

# I encapsulate an actor's response to an invocation
class ResponseMessage(object):
  def __init__(self, id, response):
    self.response = response
    self.id = id

  def __str__(self):
    return 'ResponseMessage, id = %s, result = %s' % (self.id, self.response)

# I am a 'dummy' message automatically generated when both:
# - A callback for a result has been requested
# - The result arrives
class CallbackMessage(object):
  def __init__(self, name, result, *args, **kwds):
    self.name = name
    self.result = result
    self.args = args
    self.kwds = kwds
  def __str__(self):
    return 'CallbackMessage, name = %s, result = %s' % (self.name, self.result)

class ActorJoinMessage(object):
  def __init__(self, name, data):
    self.name = name
    self.data = data
  def __str__(self):
    return 'ActorJoinMessage, name = %s, data = %s' % (self.name, self.data)
  
class SpecialMessage(object):
  def __init__(self, name, data, kwds):
    self.name = name
    self.data = data
    self.kwds = kwds
    
  def __str__(self):
    return 'SpecialMessage, name = %s, data = %s' % (self.name, self.data)