from Swan.swanjs.visitor import SwanVisitor
from compiler.visitor import ExampleASTVisitor
from compiler import parseFile, walk
import sys, os

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
				

if __name__ == '__main__':
	if sys.argv[1] == "test":
		translateTest(sys.stdout)
	else:	
		modulepaths = sys.argv[1:]
	
		modules = enqueueModules(modulepaths)#map(lambda x: (getModuleName(x), x), modulepaths)
		mainmodule = modules[0][0]
		outputname = "%s.html" % modules[0][0]
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

		stubloc = "%s/stub.html" % os.path.dirname(sys.argv[0])
		stubloc = stubloc if stubloc.startswith(os.getcwd()) else os.getcwd() +"/" + stubloc
		base = open(stubloc, 'r').read()
		base = base.replace("%%compilation%%", compilation)
		base = base.replace("%%modulename%%", mainmodule)
		
		outputfile = open(outputname, 'w')
		outputfile.write(base)
		outputfile.close()
		print "Output written to %s" % outputname