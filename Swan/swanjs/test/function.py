def simple():
	pass

def withArg(arg1):
	pass

def withDef(arg1, arg2=2, arg3=3):
	pass

def withVarargs(arg1, *varargs):
	a = True
	pass

def withKwdargs(arg1, **kwdargs):
	pass

def withAll(arg1, arg2, arg3=2, *varargs, **kwdargs):
	pass

def return_(a, b):
	return a * b
	
a = lambda **x : x + 5

# simple()
# comp[l].ex()
# withArg(5*5)
# withDef(5)
# withDef(5, 5)
# withVarargs(5, 1,2,3,4)
# withKwdargs(5, asdf="zxcv")
# withAll(5,2, *vargs, **kargs)
