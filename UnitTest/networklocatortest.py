import unittest
from Manager.locator import *

TEST_PORT = 6022

class ManagerExternalInterfaceTest(unittest.TestCase):

  def testLocator(self):
    locator = ManagerExternalInterface()
    locator.actoris('some-actor', TheatreReference('somewhere', 600))
    t = locator.whereis('some-actor')
    self.assertEqual('somewhere', t.address)
    self.assertEqual(600, t.port)
    
  def testMissingActor(self):
    locator = ManagerExternalInterface()
    t = locator.whereis('some-actor')
    self.assertEqual(None, t)

  def testOverwritingLocation(self):
    locator = ManagerExternalInterface()
    locator.actoris('some-actor', TheatreReference('somewhere', 600))
    locator.actoris('some-actor', TheatreReference('somewhere-else', 700))
    t = locator.whereis('some-actor')
    self.assertEqual('somewhere-else', t.address)
    self.assertEqual(700, t.port)
    
  def testLocatingGlobalActor(self):
    locator = ManagerExternalInterface()
    existing = locator.globalactoris('global-actor', TheatreReference('somewhere', 600))
    self.assertEqual(None, existing)
    t = locator.whereis('global-actor')
    self.assertEqual('somewhere', t.address)
    self.assertEqual(600, t.port)
    
  def testRegisteringExistingGlobalActor(self):
    locator = ManagerExternalInterface()
    locator.globalactoris('global-actor', TheatreReference('somewhere', 600))
    existing = locator.globalactoris('global-actor', TheatreReference('somewhere-else', 700))
    
    self.assertEqual('somewhere', existing.address)
    self.assertEqual(600, existing.port)
   
  def testDeadActor(self):
    locator = ManagerExternalInterface()
    locator.actoris('some-actor', TheatreReference('somewhere', 600))
    locator.isdead('some-actor')
    t = locator.whereis('some-actor')
    self.assertEqual(None, t)
    
  def testDeadMissingActor(self):
    # Killing an acor that doesn't exist should not raise
    # an error since there's nothing that a host can do about it
    locator = ManagerExternalInterface()
    locator.isdead('some-actor')  