from Messaging.structures import MessageQueue, ResultMap
from Messaging.message import *

class MessageStore(object):
  def __init__(self):
    self.__requests = MessageQueue()
    self.__responses = ResultMap()
    self.__last_req_id = 0
    self.__callbacks = dict()
    self.offers = 0
    self.split = 0
    
  def __len__(self):
    return len(self.__requests)

  def add_front(self, name, args, kwds):
    self.__requests.add_front(SpecialMessage(name, args, kwds))

  def get_next_request(self):
    return self.__requests.get_next()

  def __add_callback_result(self, method, result, *args, **kwds):
    message = CallbackMessage(method, result, *args, **kwds)
    self.__requests.add(message) 
 
  def __request_callback(self, request_id, method, *args, **kwds):
    self.__callbacks[request_id] = (method, args, kwds)
 
  def add_callback(self, method, request_id, *args, **kwds):
    message = self.__responses.get_async(request_id)
    if message:
      # We already have the result, add the result into the incoming
      # queue.
      self.__add_callback_result(method, message.response, *args, **kwds)
    else:
      self.__request_callback(request_id, method, *args, **kwds) 

  def wait_for_result(self, request_id):
    return self.__responses.wait_for(request_id).response

  def add(self, message): 
    if type(message) == RequestMessage:
      # TODO: reverse dependancy? would be nicer if actor
      # called add_front, but at the moment add_front only
      # deals with special messages- change help_offer to
      # be special, or change others so they aren't
      if message.name == 'help_offer':
        self.__requests.add_front(message)
        self.offers += 1
      elif message.name == 'add_all':
        for msg in message.args:
          self.__requests.extend(msg)
      else:
        self.__requests.add(message)
    elif type(message) == ResponseMessage:
      if (self.__callbacks.has_key(message.id)):
        meth, args, kwds = self.__callbacks[message.id]
        #meth = self.__callbacks[message.id]
        del self.__callbacks[message.id]
        self.__add_callback_result(meth, message.response, *args, **kwds)
      else:
        self.__responses.add(message)
    elif type(message) == ActorJoinMessage:
        self.__requests.add(message)
    else:
      raise MessageRejectedException(self, message)
      
  def get_messages(self, start, finish):
    return self.__requests.get_messages(start, finish)

  def has_result(self, request_id):
    return self.__responses.has_result(request_id)
  
  def new_request(self):
    self.__last_req_id += 1
    return self.__last_req_id

  def new_request(self):
    self.__last_req_id += 1
    return self.__last_req_id

class MessageRejectedException(Exception):
  def __init__(self, actor, message):
    Exception.__init__(self, "actors do not accept messages of this type: '%s'" %  message)