import unittest
import sets
from Actors.messagestore import MessageStore, MessageRejectedException
from Messaging.message import RequestMessage, ResponseMessage, CallbackMessage

class TestActorMessageHandling(unittest.TestCase):
  
  def setUp(self):
    self.request_a = RequestMessage(10, 'method-a', [5], [])
    self.response_a = ResponseMessage(10, 'ok')
    self.request_b = RequestMessage(11, 'method-b', ['arg1', 'arg2'])
    self.response_b = ResponseMessage(11, 'ok')
    self.messages = MessageStore()
    
  def testGetNextRequest(self):
    self.messages.add(self.request_a)
    self.messages.add(self.request_b)
    first = self.messages.get_next_request()
    self.assertEqual(self.request_a, first)
    second = self.messages.get_next_request()
    self.assertEqual(self.request_b, second)
    
  def testCallbackRequestWhenResponseNotYetIn(self):
     self.messages.add_callback('method', 10)
     self.messages.add(self.response_a)
     callback = self.messages.get_next_request()
     self.assertEqual('method', callback.name)
     self.assertEqual(self.response_a.response, callback.result)
     
  def testCallbackRequestWhenResponseAlreadyIn(self):
     self.messages.add(self.response_a)
     self.messages.add_callback('method', 10)
     callback = self.messages.get_next_request()
     self.assertEqual('method', callback.name)
     self.assertEqual(self.response_a.response, callback.result)

  def testResponse(self):
    self.messages.add(self.request_a)
    self.messages.add(self.request_b)
    self.messages.add(self.response_b)
    self.messages.add(self.response_a)
    response = self.messages.wait_for_result(self.request_b.id)
    self.assertEqual(self.response_b.response, response)
    response = self.messages.wait_for_result(self.request_a.id)
    self.assertEqual(self.response_a.response, response)

  def testHasResult(self):
    self.messages.add(self.request_a)
    self.messages.add(self.request_b)
    self.assertFalse(self.messages.has_result(10))
    self.assertFalse(self.messages.has_result(11))
    self.messages.add(self.response_b)
    self.assertFalse(self.messages.has_result(10))
    self.assertTrue(self.messages.has_result(11))
    
  def testGettingNewRequestId(self):
    ids = [self.messages.new_request() for i in range(0,20)]
    unique_ids = sets.Set(ids)
    self.assertEqual(len(unique_ids), len(ids))
    
  def testInvalidMessage(self):
    try:
      self.messages.add('John')
      self.fail('Exception expected')
    except MessageRejectedException:
      pass     