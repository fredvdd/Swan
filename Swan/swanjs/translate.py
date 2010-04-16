from Swan.swanjs.visitor import SwanVisitor
from compiler.visitor import ExampleASTVisitor
from compiler import parse, parseFile, walk
import sys, os

class Buffer():
	
	def __init__(self):
		self.acc = ""
		
	def write(self, mess):
		self.acc += mess

def translate(modulename, modulepath, outstream):	
	ast = parseFile(modulepath)
	v = SwanVisitor(modulename, outstream)
	w = ExampleASTVisitor()
	w.VERBOSE = 1
	walk(ast, v, v)
	return (v.deps, v.out)
		
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
	
def getModuleName(modulepath):
	path, name = os.path.split(modulepath)
	path = os.getcwd() + "/" + path
	if path not in sys.path:
		sys.path.insert(0, path)
	return name.split('.')[0]
	
def unravel(buffs):
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
	
		modules = map(lambda x: (getModuleName(x), x), modulepaths)
		mainmodule = modules[0][0]
		outputname = "%s.html" % modules[0][0]
		done = []
		buffers = []
		while modules:
			modulename, modulepath = modules.pop(0)
			more, res = translate(modulename, modulepath, Buffer())
			
			done.append(modulepath)
			print "Done %s, need %s" % (modulename, more)
			
			morepaths = [findpath(x) for x in more]
			for mod, modpath in zip(more, morepaths):
				if modpath not in done and (mod,modpath) not in modules:
					modules.append((mod,modpath))
				else:
					pass#print "Already done %s" % mod
			buffers.append((modulepath, morepaths, res))
	
		compilation = "mainmodule = '%s'\n\n" % mainmodule
		buffers = unravel(buffers)
		while buffers:
			path, more, buff = buffers.pop(0)
			print "Module: " + path
			compilation += "//**** Module: %s ****//\n" % (os.path.basename(path))
			compilation += buff.acc
			compilation += "//** End Module: %s **//\n\n" % (os.path.basename(path))

		base = open("%s/%s/stub.html" % (os.getcwd(), os.path.dirname(sys.argv[0])), 'r').read()
		base = base.replace("%%compilation%%", compilation)
		base = base.replace("%%modulename%%", mainmodule)
	
		outputfile = open(outputname, 'w')
		outputfile.write(base)
		outputfile.close()