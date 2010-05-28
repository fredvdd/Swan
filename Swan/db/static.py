from Swan.db.model import Model, ModelInstance
from Swan.db.fields import *
from Swan.db.relation import ForeignRelation
from inspect import isclass
import types
import Swan

def extract_models(modelpath):
	print "Extracting models from " + modelpath
	module = __import__(modelpath, globals(), locals(), [''])
	models = {}
	for x in dir(module):
		 if isclass(module.__dict__[x]) and issubclass(module.__dict__[x], Model):
			models[x] = module.__dict__[x]													
	return models


def init_db_models(modelpath):
	models = extract_models(modelpath)
	print "Initialising models %s" % [x for x in models]
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
						rel = ForeignRelation(model, models[model], e, fk.table, models[fk.table])
						fkss[fk.table].update({fk.name:rel})
						fields[e]=rel
			else:
				break
		fieldss[model] = fields
	for model in models:
		funcss[model].update(fkss[model])
		# funcss[model].update({'__fields':fieldss[model]})
		n = models[model].__name__ +"Instance"
		t = type(n, (ModelInstance,), funcss[model])
		setattr(t, '__fields', fieldss[model])
		setattr(Swan.db.static, n, t) #This is a slightly ridiculous requirement, needed for pickling...
		models[model].instance_type = t
	return models
