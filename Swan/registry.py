from Actors.keywords import *
import re

class Registry(StaticActor):
	
	def birth(self):
		self.registry = {} #regex -> handler [specifier]

	def print_registry(self):
		print self.registry
	
	def lookup(self, key):
		for regex, resp in self.registry.iteritems():
			match = regex.match(key)
			if match:
				return (resp[0],resp[1],match.groupdict())
	
	def register(self, key, value, specifier=None):
		self.registry[re.compile(key)] = (value, None)
