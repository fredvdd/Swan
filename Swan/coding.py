from json import JSONEncoder, dumps, loads
from Swan.db import *
from Swan.static import log

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
		return self.encode(content)
	
	def encodeModel(self, model):
		fields = getattr(model.__class__, '__fields')
		return dict([(f,getattr(model,f)) for (f,t) in fields.iteritems() if not isinstance(t, ForeignRelation)])

	def default(self, obj):
		if isinstance(obj, ModelInstance):
			return self.encodeModel(obj)
		if isinstance(obj, RelationSet) or isinstance(obj, Query):
			return list(obj.__iter__())
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
		return dict([(str(k),v) for (k,v) in loads(encoded).iteritems()])

encoders = dict({'application/json':SwanJSONEncoder})
decoders = dict({'application/json':SwanJSONDecoder})