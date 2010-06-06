from Swan.server import Handler, FileHandler
from Actors.keywords import MobileActor, find_type
from models import * 
from datetime import datetime

class RootHandler(FileHandler):
	root = "/files/"
	bindings = {"default":"/kennel/`path`?"}

class Kennel(Handler):
	bindings = {'default':'/dogs/?'}

	def birth(self):
		self.central = find_type('DogList')

	def get(self): #list the dogs in the kennel 
		response.send(200, self.central.get_list(), 'application/json')

	def post(self, body):#add a dog to the kennel 
		self.central.append(body)
		response.send(204)

class DogList(MobileActor):
	
	def birth(self):
		self.list = list()
		
	def get_list(self):
		return self.list

	def append(self, dog):
		self.list.append(dog)
	
	
# POST /dogs/ HTTP/1.1
# content-type:text/plain
# content-length: 5
# 
# Rover

# GET /dogs/ HTTP/1.1
	
	
		