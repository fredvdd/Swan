from Actors.keywords import *

class EventBroker(MobileActor):
  
  def birth(self):
    self.subscribers = dict()
    
  def subscribe(self, event, method):
    subscribers = self.getsubscribers(event)
    subscribers.append(method)
    self.subscribers[event] = subscribers
    
  def publish(self, event, *args):
    subscribed = self.getsubscribers(event)
    for subscriber in subscribed:
      subscriber(*args)
    
  def getsubscribers(self, event):
    if not event in self.subscribers:
      return []
    else:
      return self.subscribers[event]