from json import JSONEncoder, dumps, loads
from Swan.db import *
from Swan.static import log
from types import NoneType, UnicodeType, ListType, DictType

class SwanEncoder(object):
	
	def __init__(self):
		pass
		
	def get_encoding(self, content):
		if isinstance(obj, ModelInstance):
			return self.encodeModel(obj)
		if isinstance(obj, RelationSet) or isinstance(obj, Query):
			return self.encodeSet(obj)
	
	def encodeModel(self, model):
		pass

	def encodeSet(self, modelset):
		pass
		
class PassThroughEncoder(SwanEncoder):
	
	def get_encoding(self,content):
		return content

class SwanJSONEncoder(SwanEncoder, JSONEncoder):
      
	def __init__(self, *args, **kwds):
		JSONEncoder.__init__(self, *args, **kwds)
		
	def get_encoding(self, content):
		if content:
			return self.encode(content)
		else:
			return "{}"
	
	def encodeModel(self, model, depth):
		fields = getattr(model.__class__, '__fields')
		objdict = dict()
		for (f,t) in fields.iteritems():
			if not  isinstance(t, ForeignRelation):
				objdict[f] = getattr(model,f)
			elif depth > 0:
				fr = getattr(model,f)
				if isinstance(fr, ModelInstance):
					objdict[f] = self.encodeModel(fr, depth-1)
		return objdict
		# return dict([(f,getattr(model,f)) for (f,t) in fields.iteritems() if not isinstance(t, ForeignRelation)])

	def default(self, obj):
		if isinstance(obj, PotentialModelInstance):
			obj._check_cache()
			return self.encodeModel(obj.cache, 0)	
		if isinstance(obj, ModelInstance):
			return self.encodeModel(obj, 1)
		if isinstance(obj, RelationSet) or isinstance(obj, Query):
			return list(obj.__iter__())
		else:
			return str(obj)
		return JSONEncoder.default(self,obj)
		
class SwanDecoder(object):
	
	def __init__(self):
		pass
		
	def get_decoding(self,encoded):
		pass
		
class PassThroughDecoder(SwanDecoder):
	
	def get_decoding(self, encoded):
		return encoded

class SwanJSONDecoder(object):
	
	def get_decoding(self,encoded):
		# print encoded
		# print type(encoded)
		content = loads(encoded)
		# print type(content)
		if isinstance(content, UnicodeType):
			return str(content)
		elif isinstance(content, DictType):
			return self.processDict(content)
		else:
			return self.processList(content)
		
	def processDict(self, content):
		return dict([(str(k),v) for (k,v) in loads(encoded).iteritems()])

	def processList(self, content):
		return map(lambda x: str(x) if isinstance(x, UnicodeType) else processDict(x), content)

encoders = dict({'application/json':SwanJSONEncoder})
decoders = dict({'application/json':SwanJSONDecoder})