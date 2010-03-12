from compiler.visitor import ASTVisitor

class SwanVisitor(ASTVisitor):
	
	def __init__(self, outstream):
		ASTVisitor.__init__(self)
		self.out = outstream
		self.opdict = {	'<' : '__lt__', '<=':'__le__', '==':'__eq__', 
					'!=':'__ne__', '>':'__gt__', '>=':'__ge__', 
					'is':'is_', 'is not':'is_not', 'in':'__contains__',
					'+=':'__iadd__', '&=':'iand', '/=':'idiv', '//=':'ifloordiv',
					'<<=':'__ilshift__', '%=':'__imod__', '*=':'__imul__',
					'|=':'__ior__','**=':'__ipow__', '>>=':'__irshift__','-=':'__isub__',
					'^=':'__ixor__'}
		self.funcVargs = 4
		self.funcKargs = 8
	
	def binOp(self, node, op):
		left, right = node.left, node.right
		self.dispatch(left)
		self.out.write(".__"+op+"__(")
		self.dispatch(right)
		self.out.write(")")
		
	#Arithmetic ops
	#The ** operator
	def visitPower(self, node):
		self.binOp(node, "pow")
			
	#The / operator	
	def visitDiv(self, node):
		self.binOp(node, "div")
	
	#The % operator 
	def visitMod(self, node):
		self.binOp(node, "mod")
			
	#The // operator
	def visitFloorDiv(self, node):
		self.binOp(node, "floordiv")
	
	#The * operator
	def visitMul(self, node):
		self.binOp(node, "mul")
	
	#The + operator
	def visitAdd(self, node):
		self.binOp(node, "add")
			
    #The - operator
	def visitSub(self, node):
		self.binOp(node, "sub")

	#As in a = +b
	def visitUnaryAdd(self, node):
		self.dispatch(node.expr)
		self.out.write(".__pos__()")

	#As in a = -b		
	def visitUnarySub(self, node):
		self.dispatch(expr)
		self.out.write(".__neg__()")
			
	#Bitwise ops &, |, ^, ~, << and >>
	def visitBitand(self, node):
		self.binOp(node, "and")

	def visitBitor(self, node):
		self.binOp(node, "or")

	def visitBitxor(self, node):
		self.binOp(node, "xor")
			
	def visitLeftShift(self, node):
		self.binOp(node, "lshift")

	def visitRightShift(self, node):
		self.binOp(node, "rshift")
		
	def visitInvert(self, node):
		self.dispatch(node.expr)
		self.out.write(".__inv__()")

	#Boolean ops : not, or, and	and comparison	
	def visitNot(self, node):
		self.out.write("!")
		self.dispatch(node.expr)

	def visitOr(self, node):
		for n in node.nodes:
			self.dispatch(n)
			self.out.write("||")

	def visitAnd(self, node):
		for n in node.nodes:
			self.dispatch(n)
			self.out.write("&&")

	def visitCompare(self, node):
		self.dispatch(node.expr)
		for op,expr in node.ops:
			self.out.write("."+self.opdict[op]+"(")
			self.dispatch(expr)
			self.out.write(")")

	#Assignment	
	def visitAssign(self, node):
		for n in node.nodes:
			self.dispatch(n, node.expr)

	def visitAssName(self, node, expr):
		self.out.write(node.name)
		if expr:
			self.out.write(" = ")
			self.dispatch(expr)
			
	def visitAssAttr(self, node, expr):
		self.dispatch(node.expr)
		self.out.write("."+node.attrname)
		if expr:
			self.out.write(" = ")
			self.dispatch(expr)

	def visitAssList(self, node, expr):
		self.out.write("lambda = ")
		self.dispatch(expr) #should evaluate to a array
		self.out.write("\n")
		i = 0
		for x in node.nodes:
			self.dispatch(x, None) 
			self.out.write(" = lambda[" + str(i) +"]\n")
			i += 1

	def visitAssTuple(self, node, expr):
		self.out.write("lambda = ")
		self.dispatch(expr) #should evaluate to a array
		self.out.write("\n")
		i = 0
		for x in node.nodes:
			self.dispatch(x, None) 
			self.out.write(" = lambda[" + str(i) +"]\n")
			i += 1

	def visitAugAssign(self, node):
		self.dispatch(node.node)
		self.out.write("." + self.opdict[node.op] + "(")
		self.dispatch(node.expr)
		self.out.write(")")
	
	def visitAssert(self, node):
		print "Visiting a Assert node"
		for n in node.getChildNodes():
			self.dispatch(n)

	# doing `object` is apparently repr(object)
	def visitBackquote(self, node):
		print "Visiting a Backquote node"
		self.dispatch(node.expr)
		self.out.write(".__repr__()")

	def visitCallFunc(self, node):
		print "Visiting a CallFunc node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Need to check out Javascript inheritance?
	def visitClass(self, node):
		print "Visiting a Class node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitGetattr(self, node):
		self.dispatch(node.expr)
		self.out.write("." + node.attrname)
	
	def visitLambda(self, node):
		print "Visiting a Lambda node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitFunction(self, node):
		self.out.write("function " + node.name + "(")
		if node.argnames:
			for name in node.argnames[:-1]:		
				self.out.write(name + ",")
			self.out.write(node.argnames[-1])
		self.out.write("){\n")
		if (node.flags & self.funcVargs) and (node.flags & self.funcKargs):
			self.out.write(node.argnames[-2]+"=arguments.slice("+str(len(node.argnames)-2)+",-1);\n")
		elif node.flags & self.funcVargs:
			self.out.write(node.argnames[-2]+"=arguments.slice("+str(len(node.argnames)-1)+");\n")
		elif node.flags & self.funcKargs:
			pass #may need to do something here. may not.
		self.dispatch(node.code)
		self.out.write("};")
		
			
	def visitReturn(self, node):
		self.out.write("return ")
		self.dispatch(node.value)
		self.out.write(";")
			
	def visitExpression(self, node):
		print "Visiting a Expression node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#A statement
	def visitStmt(self, node):
		for n in node.getChildNodes():
			self.dispatch(n)
			self.out.write("\n")

	def visitDecorators(self, node):
		print "Visiting a Decorators node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitDiscard(self, node):
		print "Visiting a Discard node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitExec(self, node):
		print "Visiting a Exec node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitIf(self, node):
		test, stmts = node.tests[0]
		self.out.write("if(")
		self.dispatch(test)
		self.out.write("){\n")
		self.dispatch(stmts)
		self.out.write("} ")
		for test, stmts in node.tests[1:]:#handles the elifs
			self.out.write("else if(")
			self.dispatch(test)
			self.out.write("){\n")
			self.dispatch(stmts)
			self.out.write("\n}")
		if node.else_:
			self.out.write(" else {\n")
			self.dispatch(node.else_)
			self.out.write("}\n")

	#Loops
	def visitFor(self, node):
		self.out.write('lambda = ')
		self.dispatch(node.list)
		self.out.write("\nfor (x in lambda){\n")
		self.dispatch(node.assign, None)
		self.out.write(" = lambda[x]\n")
		self.dispatch(node.body)
		self.out.write("}\n")
		if node.else_:
			self.dispatch(node.else_)
			
	def visitBreak(self, node):
		self.out.write("break")

	def visitContinue(self, node):
		self.out.write("continue")

	def visitWhile(self, node):
		self.out.write("while(")
		self.dispatch(node.test)
		self.out.write("){\n")
		self.dispatch(node.body)
		self.out.write("}\n")
		if node.else_:
			self.dispatch(node.else_)
	
	#Not sure there's an equivalence for this in JS
	def visitYield(self, node):
		print "Visiting a Yield node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitGenExpr(self, node):
		print "Visiting a GenExpr node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitGenExprFor(self, node):
		print "Visiting a GenExprFor node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitGenExprIf(self, node):
		print "Visiting a GenExprIf node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitGenExprInner(self, node):
		print "Visiting a GenExprInner node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitGlobal(self, node):
		print "Visiting a Global node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Importing
	def visitImport(self, node):
		print "Visiting a Import node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitFrom(self, node):
		print "Visiting a From node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitModule(self, node):
		print "Visiting a Module node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitName(self, node):
		if node.name in ["True", "False"]:
			node.name = node.name.lower()
		self.out.write(node.name)

	def visitKeyword(self, node):
		print "Visiting a Keyword node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitConst(self, node):
		self.out.write("%s" % node.value)

	def visitDict(self, node):
		print "Visiting a Dict node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitTuple(self, node):
		print "Visiting a Tuple node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitList(self, node):
		self.out.write("[")
		for n in node.nodes:
			self.dispatch(n)
		self.out.write("]")

	def visitListComp(self, node):
		print "Visiting a ListComp node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitListCompFor(self, node):
		print "Visiting a ListCompFor node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitListCompIf(self, node):
		print "Visiting a ListCompIf node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Pass
	def visitPass(self, node):
		self.out.write("//no-op pass")

	#Print with no \n
	def visitPrint(self, node):
		print "Visiting a Print node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#Print with \n
	def visitPrintnl(self, node):
		print "Visiting a Printnl node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#From "asdf"[1:3]		
	def visitSlice(self, node):
		print "Visiting a Slice node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#From "asdf"[1:3:4]
	def visitSliceobj(self, node):
		print "Visiting a Sliceobj node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Dictionary/Tuple access
	def visitSubscript(self, node):
		print "Visiting a Subscript node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Try/exceptions
	def visitTryExcept(self, node):
		print "Visiting a TryExcept node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitTryFinally(self, node):
		print "Visiting a TryFinally node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitRaise(self, node):
		print "Visiting a Raise node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#The with keyword.
	def visitWith(self, node):
		print "Visiting a With node"
		for n in node.getChildNodes():
			self.dispatch(n)
