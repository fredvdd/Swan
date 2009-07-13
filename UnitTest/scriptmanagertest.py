import unittest
import inspect
from Host.Migration.script import *
from Data.someactor import SomeActor
class TestScriptManager(unittest.TestCase):
  
  def testEmptyManager(self):
    manager = ScriptManager()
    self.assertFalse(manager.has_script('a module'))
  
  def testAddScript(self):
    s= SomeActor()
    module =  inspect.getmodule(s)
    src = inspect.getsource(module)
    manager = ScriptManager()        
    manager.add_script(module.__name__, src)    
    self.assertFalse(manager.has_script('Data.actor'))