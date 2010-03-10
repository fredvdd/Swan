from Swan.swanjs.visitor import SwanVisitor
from compiler.visitor import ExampleASTVisitor
from compiler import parse, parseFile, walk
import sys


def translate(modulename, outstream):
	
		ast = parseFile(modulename)
		v = SwanVisitor(outstream)
		w = ExampleASTVisitor()
		w.VERBOSE = 1
		walk(ast, v, v)
		print

if __name__ == '__main__':
	modulename = sys.argv[1]
	translate(modulename, sys.stdout)