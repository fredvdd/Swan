from threading import Condition

class ResultMap(object):
  def __init__(self):
    self.__results = dict()
    self.__cm = Condition()

  def __getstate__(self):
    return [self.__results]
  
  def __setstate__(self, state):
    self.__results = state[0]
    self.__cm = Condition()

  def add(self, message):
    self.__cm.acquire()
    self.__results[message.id] = message
    self.__cm.notify()
    self.__cm.release()

  def wait_for(self, id):
    self.__cm.acquire()
    while not self.__results.has_key(id):
      self.__cm.wait()
    response = self.__results[id]
    del self.__results[id]
    self.__cm.release()
    return response

  def has_result(self, id):
    self.__cm.acquire()
    result = self.__results.has_key(id)
    self.__cm.release()
    return result

  def get_async(self, id):
    self.__cm.acquire()
    result = None
    if self.__results.has_key(id):
      result = self.__results[id]
      del self.__results[id]
    self.__cm.release()
    return result

class MessageQueue(object):
  def __init__(self):
    self.__messages = []
    self.__special_messages = []
    self.__cm = Condition()
  
  def __len__(self):
    return len(self.__messages)
    
  def __getstate__(self):
    return [self.__messages]
  
  def __setstate__(self, state):
    self.__messages = state[0]
    self.__cm = Condition()
    
  def add_front(self, message):  
    self.__cm.acquire()
    self.__special_messages.insert(0, message)
    self.__cm.notify()
    self.__cm.release()
  
  def extend(self, messages):
    self.__cm.acquire()
    self.__messages.extend(messages)
    self.__cm.notify()
    self.__cm.release()
  
  def add(self, message):
    self.__cm.acquire()
    self.__messages.append(message)
    self.__cm.notify()
    self.__cm.release()
    
  def get_messages(self, start, finish):
    self.__cm.acquire()
    sub_messages = self.__messages[start:finish]
    del self.__messages[start:finish]
    self.__cm.notify()
    return sub_messages

  def get_next(self):
    self.__cm.acquire()
    try:
      self.__special_messages
    except AttributeError:
      self.__special_messages = []
    while len(self.__messages) == 0 and len(self.__special_messages) == 0:
      self.__cm.wait()
    if len(self.__special_messages) > 0:
      item = self.__special_messages.pop(0)
    else:
      item = self.__messages.pop(0)
    self.__cm.release()
    return item

