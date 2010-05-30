from Swan.swanjs.visitor import SwanVisitor
from compiler.visitor import ExampleASTVisitor
from compiler import parseFile, walk
import sys, os, inspect
from Swan.server import Handler

class Buffer():
	
	def __init__(self):
		self.acc = ""
		
	def write(self, mess):
		self.acc += mess
	
	def __str__(self):
		return self.acc
		
def translateTest(outstream):
	tests = os.getcwd() + "/Swan/swanjs/test"
	for test in os.listdir(tests):
		if test[-2:] == "py":
			testfile = "%s/%s" % (tests, test)
			modulename = os.path.basename(testfile).split('.')[0]
			print "##############"
			print ">>>> Translating %s (%s)" % (modulename,test)
			print "##############\n"
			translate(modulename, testfile, outstream)

def translate(modulename, modulepath, outstream):	
	ast = parseFile(modulepath)
	v = SwanVisitor(modulename, outstream)
	w = ExampleASTVisitor()
	w.VERBOSE = 1
	walk(ast, v, v)
	#print v.out
	return (v.deps, v.out)
			
def findpath(modname):
	modname = modname.replace(".", "/")
	for path in sys.path:
		modpath = "%s/%s.py" % (path, modname)
		#print "Looking for " + modpath
		if os.path.exists(modpath):
			sys.path.insert(0, os.path.dirname(modpath))
			#print "\n"
			return modpath
		altpath = "%s/%s/__init__.py" % (path, modname)
		if os.path.exists(altpath):
			sys.path.insert(0, os.path.dirname(altpath))
			return altpath
	raise ImportError("Couldn't find module " + modname)
	
def enqueueModules(modulepaths):
	modules = []
	for modulepath in modulepaths:
		path, name = os.path.split(modulepath)
		path = "%s/%s" % (os.getcwd(), path) # if not path.startswith(os.getcwd()) else path
		if path not in sys.path:
			sys.path.insert(0, path)
		modules.append((name.split('.')[0], modulepath))
	return modules
	
def unravel(buffs):
	print "Re-ordering modules..."
	orderedbuffs = [buffs[0]]
	for buf in buffs[1:]:
		name, _, _ = buf
		ins = False
		for pos, (_, deps, _) in enumerate(orderedbuffs):
			if name in deps:
				orderedbuffs.insert(pos, buf)
				ins = True
				break
		if not ins:
			orderedbuffs.append(buf)
	return orderedbuffs
	
def translate_source(modulepaths):
	modules = enqueueModules(modulepaths)#map(lambda x: (getModuleName(x), x), modulepaths)
	mainmodule = modules[0][0]
	print modules
	done = []
	buffers = []
	print "Cross-compiling: "
	while modules:
		modulename, modulepath = modules.pop(0)
		print "Module %s" % modulename
		deps, res = translate(modulename, modulepath, Buffer())
		
		done.append(modulepath)
		print "Done %s, need %s" % (modulename, deps)
		
		deppaths = [findpath(x) for x in deps]
		for mod, modpath in zip(deps, deppaths):
			if modpath not in done and modpath not in [y for (x,y) in modules]:
				modules.append((mod,modpath))
			else:
				print "Already done %s" % mod
		buffers.append((modulepath, deppaths, res))
		#print "%s" % modules
		#print "%s" % buffers

	compilation = ""
	buffers = unravel(buffers)
	while buffers:
		path, deps, buff = buffers.pop(0)
		print "Writing module: " + os.path.basename(path).split(".")[0]
		compilation += "//**** Module: %s ****//\n" % (os.path.basename(path))
		compilation += buff.acc
		compilation += "//** End Module: %s **//\n\n" % (os.path.basename(path))

	# print os.path.dirname(sys.modules['Swan.swanjs.translate'].__file__)
	stubloc = "%s/stub.html" % os.path.dirname(sys.modules['Swan.swanjs.translate'].__file__)
	stubloc = stubloc if stubloc.startswith(os.getcwd()) else os.getcwd() +"/" + stubloc
	base = open(stubloc, 'r').read()
	base = base.replace("%%compilation%%", "\n"+compilation)
	base = base.replace("%%modulename%%", "\n\t"+mainmodule)
	
	return base
	
def add_handlers(view_js, handlerpath):
	extra = """function swanjsRequest(method, path){
		this.method = method;
		this.path = path;
		this.request = new XMLHttpRequest();
	}
	
	swanjsRequest.prototype.open = function(){
		this.request.open(this.method, this.path, true)
		return this;
	}

	swanjsRequest.prototype.setHeader = function(key,value){
		this.request.setRequestHeader(key, value)
		return this
	}
	swanjsRequest.prototype.send = function(body){
		this.request.send(body)
		return this
	}\n\n
	"""
	modulename = os.path.relpath(handlerpath).replace("/",".")
	print modulename
	handlermod = __import__(modulename, globals(), locals(), [''])
	for hn in dir(handlermod):
		hc = getattr(handlermod, hn)
		if inspect.isclass(hc) and issubclass(hc, Handler):
			if hc.__name__ == 'Handler' or hc.__name__ == 'FileHandler':
				continue
			extra += hc.__name__ + " = function(){}\n"
			extra += "_ = " + hc.__name__ + ".prototype;\n"
			
			bindings = getattr(hc, 'bindings')
			for hm in dir(hc):
				if hm == 'get_method':
					continue
				for method in ['get','put','post','delete']:
					if hm.startswith(method):
						function = getattr(hc, hm)
						code =  function.func_code
						args = code.co_varnames[1:code.co_argcount] 
						extra += "_." + hm + " = function(" + reduce(lambda a,c: "%s,%s"%(a,c), args if len(args)>0 else ['']) + "){\n"
						defaults = function.func_defaults
						optional = args[len(args)-(len(defaults) if defaults else 0):]
						for arg in optional:
							extra += "\t%s = typeof(%s) != 'undefined' ? %s : '';\n" % (arg, arg, arg)
						parts = hm.split('_',1)
						method, spec = parts if len(parts)>1 else (parts[0], 'default')
						pat = bindings[spec]
						for arg in args:
							pat = pat.replace(("?`%s`?" if arg in optional else "`%s`")%arg, "'+%s+'"%arg)
						url = "'%s'"%pat.rstrip("/?")
						extra += "\treturn [new swanjsRequest('%s', %s), %s]\n"%(method, url, 'body' if method in ['put','post'] else 'null')
						extra += "};\n"
	view_js = view_js.replace("%%handlers%%", "\n"+extra)
	return view_js
		
def output_js(js, outputpath):
		outputname = "%s.html" % outputpath
		outputfile = open(outputname, 'w')
		outputfile.write(js)
		outputfile.close()
		print "Output written to %s\n\n\n" % outputname

if __name__ == '__main__':
	if sys.argv[1] == "test":
		translateTest(sys.stdout)
	else:	
		modulepaths = sys.argv[1:-1]
		output_js(translate_source(modulepaths), sys.argv[-1])
	
	