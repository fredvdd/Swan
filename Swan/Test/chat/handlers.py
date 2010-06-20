from Swan.server import Handler, FileHandler, ExternalHandler
from Actors.keywords import NamedSingletonActor, find_type
from models import *
from time import time as time_now
from json import loads
from urllib import urlencode,unquote

class RootHandler(FileHandler):
	root = "/files/"
	bindings = {"default":"/chat/?`path`?"}
	
class Messages(Handler):
	bindings = { 'default':'/messages/`name`/?`time`?'}
	
	def birth(self):
		self.hub = find_type('MessageHub')

	def get(self, name, time=None):#retrieve messages
		self.hub.get_messages(response, time)

	def post(self, name, body, time=None):#send a message
		self.hub.put_message({'time':time_now(),'name':name,'message':body,'type':'message'})
		response.send(200)

class MessageHub(NamedSingletonActor):

	def birth(self):
		self.msgs = []
		self.responses = []
		
	def put_message(self, msg):
		self.msgs.insert(0,msg)
		while self.responses:
			response = self.responses.pop().send(200,[msg])

	def get_messages(self, response, time=None):
		msgs = filter(lambda msg:msg['time']>float(time),self.msgs) if self.msgs and time else []
		if msgs:
			response.send(200,msgs)
		else:
			self.responses.append(response)
		
class Photos(ExternalHandler):
	bindings = {'photo':'/flickr/`user`/`title`'}
	
	def get_photo(self, user, title):
		fluid = User.get(name=equals(user)).flickr_uid[0].uid
		print "Looking for title " + title
		params = {	'api_key':"745bf5cec0e4c9a5e9d225ce015b2e84",
					'method':"flickr.people.getPublicPhotos",
					'user_id':fluid,
					'format':'json' }
		resp = loads(self._get_request('api.flickr.com','/services/rest/?'+urlencode(params)).read()[14:-1])
		photo = filter(lambda p:p['title']==unquote(title), resp['photos']['photo'])[0]
		photo.update({'user':user,'type':'photo','time':time_now()})
		find_type('MessageHub').put_message(photo)
		response.send(200)
