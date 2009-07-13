import unittest
from Actors.keywords import *


class SomeTest(unittest.TestCase):
  
  def testArgumentsAreByValue(self):
    DataModifier(DataStore())
  
class DataModifier(NetworkActor):
  
  def birth(self, store):
    data = sync(store.get_data())
    data.append('extra')
    store.check()
  
class DataStore(NetworkActor):
  
  def birth(self):
    self.data = [1,2,3]
  
  def get_data(self):
    return self.data

  def check(self):
    assert self.data == [1,2,3]