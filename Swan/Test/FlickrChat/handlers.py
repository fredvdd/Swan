from Swan.server import Handler, FileHandler, ExternalHandler
from Actors.keywords import NamedSingletonActor, find_type
from models import *
from time import time as time_now
from json import loads
from urllib import urlencode,unquote

class MessageHub(NamedSingletonActor):

	def birth(self):
		self.msgs = []
		self.responses = []
		
	def put_message(self, msg):
		self.msgs.insert(0,msg)
		while self.responses:
			response = self.responses.pop().send(200,[msg])

	def get_messages(self, response, time=None):
		msgs = filter(lambda msg:msg['time']>float(time),self.msgs) if (self.msgs and time) else []
		if msgs:
			response.send(200,msgs)
		else:
			self.responses.append(response)
