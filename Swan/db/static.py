from Swan.db.model import Model, ModelInstance
from Swan.db.query import ForeignRelation
from Swan.db.fields import *
from inspect import isclass
import types
import Swan

def extract_models(modelpath):
	module = __import__(modelpath, globals(), locals(), [''])
	models = {}
	for x in dir(module):
		 if isclass(module.__dict__[x]) and module.__dict__[x].__bases__[0].__name__ == "Model":
			models[x] = module.__dict__[x]													
	return models


def init_db_models(modelpath):
	print "Extracting models from " + modelpath
	models = extract_models(modelpath)
	fkss = dict([[x,{}] for x in models])
	fieldss = dict([[x,{}] for x in models])
	funcss = dict([[x,{}] for x in models])
	for model in models:
		funcss[model] = dict([(x,y) for (x,y) in models[model].__dict__.iteritems() if isinstance(y, types.FunctionType)])
		fields = {}
		for parent in models[model].__mro__:
			if issubclass(parent, Model):
				es = parent.__dict__
				for e in es:
					if isinstance(es[e], Field):
						fields[e] = es[e].__class__
					if isinstance(es[e], ForeignKey):
						fk = es[e]
						fkss[fk.table].update({fk.name:ForeignRelation(model, models[model], e)})
			else:
				break
		fieldss[model] = fields
	for model in models:
		funcss[model].update(fkss[model])
		funcss[model].update({'__fields':fieldss[model]})
		n = models[model].__name__ +"Instance"
		t = type(n, (ModelInstance,), funcss[model])
		setattr(Swan.db.static, n, t) #This is a slightly ridiculous requirement, needed for pickling...
		models[model].instance_type = t
	return models