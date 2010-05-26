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
		# print "Encoder encoding %s" % content
		dump = dumps(content, cls=SwanJSONEncoder)
		# print dump
		return dump
	
	def encodeModel(self, model):
		# log.debug(self, "Evaluating model")
		fields = getattr(model.__class__, '__fields')
		objdict = dict([(f,getattr(model,f)) for (f,t) in fields.iteritems() if not isinstance(t, ForeignRelation)])
		return JSONEncoder.encode(self, objdict)
		
	def encodeSet(self,modelset):
		# log.debug(self,"Evaluating modelset %s"%type(modelset))
		return "[" + reduce(lambda s,j:"%s,%s"%(s,j), map(self.default, modelset)) + "]"

	def default(self, obj):
		if isinstance(obj, ModelInstance):
			return self.encodeModel(obj)
		if isinstance(obj, RelationSet) or isinstance(obj, Query):
			return self.encodeSet(obj)
		return JSONEncoder.default(self,obj)

encoders = dict({'application/json':SwanJSONEncoder})