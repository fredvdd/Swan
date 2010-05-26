from Actors.keywords import *
from Swan.static import log
import re

class Registry(StaticActor):
	"""Dictionary for handlers for a URL"""
	
	def birth(self, handlers):
		self.registry = {} #regex -> (handler, [specifier])
		self.default_handlers = handlers
		self.process_pattern = re.compile('(`[a-zA-Z]+`\??)')

	def print_registry(self):
		print self.registry
	
	def lookup(self, key):
		for regex, resp in self.registry.iteritems():
			match = regex.match(key)
			if match:
				return (resp[0],resp[1],match.groupdict())
		return (self.default_handlers, None, dict())
	
	def register(self, pattern, handler, specifier=None):
		pattern = self.process(pattern)
		self.registry[re.compile(pattern)] = (handler, specifier)
	
	def process(self, pattern):
		for param in self.process_pattern.findall(pattern):
			opt = param.endswith('?')
			name = param[1:(-2 if opt else -1)]
			repl = "(?P<%s>[^/]+)" % name
			pattern = pattern.replace(param, repl+("?" if opt else ""))
		return pattern
