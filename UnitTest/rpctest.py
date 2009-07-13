import unittest
import socket
from Util.Network import rpc

TEST_PORT = 6040

class RPCTest(unittest.TestCase):
    
  def setUp(self):
    self.server = rpc.RPCValve(TEST_PORT, TestTarget())
    self.conn = rpc.RPCConnector(socket.gethostname(), TEST_PORT)
    
  def tearDown(self):
    self.server.shutdown()
    
  def testSimple(self):
    self.server.listen()
    target = self.conn.connect()
    r1 = target.add(5, 5)
    r2 = target.add(10, 5)
    self.conn.disconnect()
    self.assertEqual(10,  r1)
    self.assertEqual(15, r2)
        
  def testMissingMethod(self):
    self.server.listen()
    target = self.conn.connect()
    try:
      r1 = target.nonexistant(10, 10)
      self.fail('Exception expected')
    except rpc.RPCException:
      pass
    self.conn.disconnect()
    
  def testMissingArgs(self):
    self.server.listen()
    target = self.conn.connect()
    try:
      r1 = target.add(10)
      self.fail('Exception expected')
    except TypeError:
      pass
    self.conn.disconnect()
        
class TestTarget(object):
  def add(self, a, b):
    return a+b