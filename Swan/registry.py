from Actors.keywords import *
from Swan.static import log
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
	
	def register(self, pattern, handler, specifier=None):
		log.debug(self, "Register %s to handle %s, specifier %s" % (handler, pattern,specifier))
		self.registry[re.compile(pattern)] = (handler, specifier)
