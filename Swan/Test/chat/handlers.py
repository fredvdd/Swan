from Swan.server import Handler, FileHandler
from Actors.keywords import NamedSingletonActor, find_type
from time import time as time_now

class RootHandler(FileHandler):
	root = "/files/"
	bindings = {"default":"/chat/`path`?"}
	
class Messages(Handler):
	bindings = { 'default':'/messages/`name`/?`time`?'}
	
	def birth(self):
		self.hub = find_type('MessageHub')

	def get(self, name, time=None):#retrieve messages
		print time
		self.hub.get_messages(response, time)

	def post(self, name, body, time=None):#send a message
		self.hub.put_message(time_now(),name,body)
		response.send(200)

class MessageHub(NamedSingletonActor):

	def birth(self):
		self.msgs = []
		self.responses = []
		
	def put_message(self, time, name, message):
		msg = {'time':time,'name':name,'message':message}
		self.msgs.insert(0,msg)
		while self.responses:
			response = self.responses.pop().send(200,[msg])

	def get_messages(self, response, time=None):
		msgs = filter(lambda msg:msg['time']>float(time),self.msgs) if self.msgs and time else []
		if msgs:
			response.send(200,msgs)
		else:
			self.responses.append(response)
		
		
#GET /messages/Fred/ HTTP/1.1
# 
# POST /messages/Fred HTTP/1.1
# Content-type : text/html
# Content-length : 5
# 
# Hello