from compiler.visitor import ASTVisitor

class SwanVisitor(ASTVisitor):
	
	def __init__(self, outstream):
		ASTVisitor.__init__(self)
		self.out = outstream
	
	#Arithmetic ops
	#The ** operator
	def visitPower(self, node):
		print "Visiting a Power node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#The / operator	
	def visitDiv(self, node):
		print "Visiting a Div node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	#The % operator 
	def visitMod(self, node):
		print "Visiting a Mod node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#The // operator
	def visitFloorDiv(self, node):
		print "Visiting a FloorDiv node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	#The * operator
	def visitMul(self, node):
		print "Visiting a Mul node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	#The + operator
	def visitAdd(self, node):
		print "Visiting a Add node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
    #The - operator
	def visitSub(self, node):
		print "Visiting a Sub node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#As in a = +b
	def visitUnaryAdd(self, node):
		print "Visiting a UnaryAdd node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#As in a = -b		
	def visitUnarySub(self, node):
		print "Visiting a UnarySub node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	#Boolean ops : not, or, and	and comparison	
	def visitNot(self, node):
		print "Visiting a Not node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitOr(self, node):
		print "Visiting a Or node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitAnd(self, node):
		print "Visiting a And node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitCompare(self, node):
		print "Visiting a Compare node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
			
	#Bitwise ops &, |, ^, ~, << and >>
	def visitBitand(self, node):
		print "Visiting a Bitand node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitBitor(self, node):
		print "Visiting a Bitor node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitBitxor(self, node):
		print "Visiting a Bitxor node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitInvert(self, node):
		print "Visiting a Invert node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitLeftShift(self, node):
		print "Visiting a LeftShift node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitRightShift(self, node):
		print "Visiting a RightShift node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#Assignment		
	def visitAssAttr(self, node):
		print "Visiting a AssAttr node"
		for n in node.getChildNodes():
			self.dispatch(n)

		for n in node.getChildNodes():
			self.dispatch(n)

	def visitAssList(self, node):
		print "Visiting a AssList node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitAssName(self, node):
		print "Visiting a AssName node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitAssTuple(self, node):
		print "Visiting a AssTuple node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitAssign(self, node):
		print "Visiting a Assign node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitAugAssign(self, node):
		print "Visiting a AugAssign node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	def visitAssert(self, node):
		print "Visiting a Assert node"
		for n in node.getChildNodes():
			self.dispatch(n)

	# doing `object` is apparently repr(object)
	def visitBackquote(self, node):
		print "Visiting a Backquote node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitCallFunc(self, node):
		print "Visiting a CallFunc node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitClass(self, node):
		print "Visiting a Class node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitGetattr(self, node):
		print "Visiting a Getattr node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	def visitLambda(self, node):
		print "Visiting a Lambda node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitFunction(self, node):
		print "Visiting a Function node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitReturn(self, node):
		print "Visiting a Return node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitConst(self, node):
		print "Visiting a Const node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitExpression(self, node):
		print "Visiting a Expression node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#A statement
	def visitStmt(self, node):
		print "Visiting a Stmt node"
		for n in node.getChildNodes():
			self.dispatch(n)

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
		print "Visiting a If node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Loops
	def visitFor(self, node):
		print "Visiting a For node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	def visitBreak(self, node):
		print "Visiting a Break node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitContinue(self, node):
		print "Visiting a Continue node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitWhile(self, node):
		print "Visiting a While node"
		for n in node.getChildNodes():
			self.dispatch(n)

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
		print "Visiting a Name node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitKeyword(self, node):
		print "Visiting a Keyword node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitDict(self, node):
		print "Visiting a Dict node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitTuple(self, node):
		print "Visiting a Tuple node"
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitList(self, node):
		print "Visiting a List node"
		for n in node.getChildNodes():
			self.dispatch(n)

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
		print "Visiting a Pass node"
		for n in node.getChildNodes():
			self.dispatch(n)

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
