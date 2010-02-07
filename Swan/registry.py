from Actors.keywords import *
import re

class Registry(StaticActor):
	
	def birth(self):
		self.register = {} #regex -> handler [specifier]
	
	def lookup(self, key):
		for (regex, resp) in self.register:
			match = regex.match(key)
			if match:
				if len(resp) > 1:
					return (resp[0],resp[1],match.groupdict())
				else:
					return (resp, None, match.groupdict())
	
	def register(self, key, value):
		self.register[re.compile(key)] = value