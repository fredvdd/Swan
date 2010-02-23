from Actors.keywords import *
import re

class Registry(StaticActor):
	"""Dictionary for handlers for a URL"""
	
	def birth(self, handlers):
		self.registry = {} #regex -> (handler, [specifier])
		self.default_handlers = handlers

	def print_registry(self):
		print self.registry
	
	def lookup(self, key):
		for regex, resp in self.registry.iteritems():
			match = regex.match(key)
			if match:
				return (resp[0],resp[1],match.groupdict())
		return (self.default_handlers, None, dict())
	
	def register(self, key, value, specifier=None):
		self.registry[re.compile(key)] = (value, None)
