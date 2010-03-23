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
			modulename = testfile.split('/')[-1].split('.')[0]
			print "##############"
			print ">>>> Translating %s" % test
			print "##############\n"
			translate(modulename, testfile, outstream)
			
def findpath(modname):
	for path in sys.path:
		modpath = "%s/%s.py" % (path, modname)
		print "Looking for " + modpath
		if os.path.exists(modpath):
			return modpath
	raise ImportError("Couldn't find module " + modname)
	
def getModuleName(modulepath):
	pathparts = modulepath.split('/')
	path = os.getcwd() + "/" + '/'.join(pathparts[:-1])
	if path not in sys.path:
		sys.path.insert(0, path)
	return pathparts[-1].split('.')[0]

if __name__ == '__main__':
	if sys.argv[1] == "test":
		translateTest(sys.stdout)
	
	modulepaths = sys.argv[1:]
	
	modules = map(lambda x: (getModuleName(x), x), modulepaths)
	buffers = []
	while modules:
		modulename, modulepath = modules.pop()
		more, res = translate(modulename, modulepath, Buffer())
		buffers.append(res)
		modules.extend([(x, findpath(x)) for x in more])
	
	while buffers:
		print buffers.pop().acc
		
