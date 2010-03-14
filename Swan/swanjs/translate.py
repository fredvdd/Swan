from Swan.swanjs.visitor import SwanVisitor
from compiler.visitor import ExampleASTVisitor
from compiler import parse, parseFile, walk
import sys, os


def translate(modulename, outstream):	
	ast = parseFile(modulename)
	v = SwanVisitor(outstream)
	w = ExampleASTVisitor()
	w.VERBOSE = 1
	walk(ast, v, v)
	print
		
def translateTest(outstream):
	tests = os.getcwd() + "/Swan/swanjs/test"
	for test in os.listdir(tests):
		if test[-2:] == "py":
			testfile = "%s/%s" % (tests, test)
			print "##############"
			print ">>>> Translating %s" % test
			print "##############\n"
			translate(testfile, outstream)

if __name__ == '__main__':
	modulename = sys.argv[1]
	if modulename == "test":
		translateTest(sys.stdout)
	else:
		translate(modulename, sys.stdout)