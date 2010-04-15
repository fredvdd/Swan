from compiler.visitor import ASTVisitor
from compiler.ast import Keyword, Name, Sliceobj, Dict
from string import ascii_uppercase as capitals

class SwanVisitor(ASTVisitor):
	
	def __init__(self, modulename, outstream):
		ASTVisitor.__init__(self)
		self.module = modulename.split('.')[-1]
		self.out = outstream
		self.opdict = {	'<' : '__lt__', '<=':'__le__', '==':'__eq__', 
					'!=':'__ne__', '>':'__gt__', '>=':'__ge__', 
					'is':'is_', 'is not':'is_not', 'in':'__contains__',
					'+=':'__add__', '&=':'__and__', '/=':'__div__', '//=':'__floordiv__',
					'<<=':'__lshift__', '%=':'__mod__', '*=':'__mul__',
					'|=':'__or__','**=':'__pow__', '>>=':'__rshift__','-=':'__sub__',
					'^=':'__xor__'}
		self.funcVargs = 4
		self.funcKargs = 8
		self.freeVarName = "lambda" #Python keyword so won't be in use
		self.freeVar = 1 #Free var index
		self.freeUsedVars = []
		self.classes = [] #classes defined in this module
		self.functions = [] #functions defined in this module
		self.vars = [] #top level vars in this module
		self.modules = [] #imported modules
		self.imports = {} #imported functions/modules
		self.deps = []
		self.toplevel = True
		
	def takeVar(self):
		if len(self.freeUsedVars) > 0:
			return self.freeUsedVars.pop(0)
		r = self.freeVarName + str(self.freeVar)
		self.freeVar += 1
		return r
	
	def releaseVar(self, var):
		#self.freeUsedVars.append(var)
		pass
		
	#Assignment	
	def visitAssign(self, node, classPrefix=None):
		if classPrefix:
			self.out.write(classPrefix)
		for n in node.nodes:
			self.dispatch(n, node.expr)

	def visitAssName(self, node, expr=None):
		if self.toplevel:
			self.out.write(self.module + "_")
			self.vars.append(node.name)
		self.out.write(node.name)
		if expr:
			self.out.write(" = ")
			self.dispatch(expr, node.name)
			
	def visitAssAttr(self, node, expr=None):
		if expr and isinstance(expr, Dict):
			expr = self.dispatch(expr)
		self.dispatch(node.expr)
		self.out.write("."+node.attrname)
		if expr:
			self.out.write(" = ")
			self.dispatch(expr, node.expr)

	def visitAssList(self, node, expr=None):
		self.out.write("lambda = ")
		self.dispatch(expr) #should evaluate to a array
		self.out.write("\n")
		i = 0
		for x in node.nodes:
			self.dispatch(x, None) 
			self.out.write(" = lambda[" + str(i) +"]\n")
			i += 1

	def visitAssTuple(self, node, expr=None):
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
		self.out.write(" = ")
		self.dispatch(node.node)
		self.out.write("." + self.opdict[node.op] + "(")
		self.dispatch(node.expr)
		self.out.write(")")
	
	#Needs a special function...
	def visitAssert(self, node):
		print "Visiting a Assert node"
		for n in node.getChildNodes():
			self.dispatch(n)

	# doing `object` is apparently repr(object)
	def visitBackquote(self, node):
		self.dispatch(node.expr)
		self.out.write(".__repr__()")

	def visitCallFunc(self, node, *args):
		#print "callee %s, args %s, vargs %s, kargs %s" % (node.node, node.args, node.star_args, node.dstar_args)
		if isinstance(node.node, Name) and node.node.name[0] in capitals:
			self.out.write("new ")
		if isinstance(node.node, Name) and node.node.name == "native":
			self.out.write(node.args[0].value)
			return
		kwds = filter(lambda x:isinstance(x, Keyword), node.args)
		if kwds:
			taken = self.takeVar()
			self.out.write("%s = {};\n" % taken)
			for kwd in kwds:
				self.dispatch(kwd, taken)
		self.dispatch(node.node)
		self.out.write("(")
		nokwds = filter(lambda x:not isinstance(x, Keyword), node.args)
		if nokwds:
			for arg in nokwds[:-1]:
				self.dispatch(arg)
				self.out.write(", ")
			self.dispatch(nokwds[-1])
		if kwds:
			self.out.write(", %s" % taken)
			self.releaseVar(taken)
		if node.star_args:
			self.out.write(", ")
			self.dispatch(node.star_args)
		if node.dstar_args:
			self.out.write(", ")
			self.dispatch(node.dstar_args)
		self.out.write(")")
		
	def visitKeyword(self, node, var):
		self.out.write("%s.%s = " % (var, node.name))
		self.dispatch(node.expr)
		self.out.write(";\n")

	def visitDecorators(self, node):
		print "Visiting a Decorators node"
		for n in node.getChildNodes():
			self.dispatch(n)
	
	def visitLambda(self, node, assName=None):
		self.transformFunction(node)
			
	def visitFunction(self, node, classPrefix=None):
		if classPrefix:
			self.out.write(classPrefix)
		self.transformFunction(node, classPrefix)
		
	def transformFunction(self, node, classFunc=None):
		#print "Function %s, classFunc = %s, args %s, %s" % (node.name, classFunc, node.argnames, (1 if classFunc else 0)) 
		if hasattr(node, "name") and not classFunc:
			self.out.write(self.module.replace(".", "_") + "_" + node.name + " = ")
			self.functions.append(node.name)
		elif hasattr(node, "name"):
			self.out.write(node.name + " = ")
		self.out.write("function (")
		node.argnames = node.argnames[1:] if classFunc else node.argnames
		if node.argnames:
			for name in node.argnames[:-1]:		
				self.out.write(name + ",")
			self.out.write(node.argnames[-1])
		self.out.write("){\n")
		if (node.flags & self.funcVargs) and (node.flags & self.funcKargs):
			self.out.write(node.argnames[-2]+"=arguments.slice("+str(len(node.argnames)-2)+",-1);\n")
			defaultArgs = node.argnames[:-2]
		elif node.flags & self.funcVargs:
			self.out.write(node.argnames[-2]+"=arguments.slice("+str(len(node.argnames)-1)+");\n")
			defaultArgs = node.argnames[:-1]
		elif node.flags & self.funcKargs:
			defaultArgs = node.argnames[:-1]
		else:
			defaultArgs = node.argnames if len(node.argnames) > 0 else []
		defaultArgs.reverse()
		for arg in defaultArgs:
			if len(node.defaults) < 1:
				break
			self.out.write("%s = typeof(%s) != 'undefined' ? %s : " % (arg, arg, arg))
			self.dispatch(node.defaults.pop())
			self.out.write(";\n")
		self.toplevel = False
		self.dispatch(node.code)
		if not classFunc:
		 	self.toplevel = True
		self.out.write("}")
			
	def visitReturn(self, node, *args):
		self.out.write("return ")
		self.dispatch(node.value)
		self.out.write(";")

	#Need to check out Javascript inheritance?
	def visitClass(self, node, classPrefix=None):
		className = self.module.replace(".", "_") + "_" + node.name
		self.out.write(
			'function ' + className + '(){\n'
				'if('+className+'.prototype.hasOwnProperty("__init__")){\n'
					+ className + '.prototype.__init__.apply(this, arguments);\n'
				'}\n'
			'}\n')
		self.classes.append(node.name)
		if node.bases:
			self.out.write("extend(" + className + ", ")
			n = node.bases[0].name
			if n in self.classes or n in self.functions or n in self.vars:
				self.out.write(self.module.replace(".", "_") + "_")
			if n in self.imports:
				self.out.write(self.imports[n] + "_")
			self.out.write(n)
			self.out.write(");\n")
		self.out.write("_="+self.module.replace(".", "_") + "_"+node.name+".prototype\n")
		# if node.bases:
		# 	self.out.write("= ")
		# 	self.dispatch(node.bases[0])
		# 	self.out.write("();\n")
		# else:
		# 	self.out.write("\n")
		self.toplevel = False
		self.dispatch(node.code, "_.")
		self.toplevel = True
			
	def visitGetattr(self, node):
		self.dispatch(node.expr)
		if isinstance(node.expr, Name) and node.expr.name in self.modules:
			self.out.write("_" + node.attrname)
		else:
			self.out.write("." + node.attrname)
			
	def visitExpression(self, node):
		#print "Visiting a Expression node"
		for n in node.getChildNodes():
			self.dispatch(n)
			
	#A statement
	def visitStmt(self, node, classPrefix = None):
		for n in node.getChildNodes():
			if classPrefix:
				self.dispatch(n, classPrefix)
			else:
				self.dispatch(n)
			self.out.write("\n")

	def visitDiscard(self, node):
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
		taken = self.takeVar()
		self.out.write('%s = ' % taken)
		self.dispatch(node.list, taken)
		self.out.write("\nfor (x in %s){\n" % taken)
		self.out.write("if(%s.hasOwnProperty(x)){" % taken)
		self.dispatch(node.assign, None)
		self.out.write(" = %s[x]\n" % taken)
		self.dispatch(node.body)
		self.out.write("}\n}\n")
		if node.else_:
			self.dispatch(node.else_)
		self.releaseVar(taken)
			
	def visitBreak(self, node):
		self.out.write("break;")

	def visitContinue(self, node):
		self.out.write("continue;")

	def visitWhile(self, node):
		self.out.write("while(")
		self.dispatch(node.test)
		self.out.write("){\n")
		self.dispatch(node.body)
		self.out.write("}\n")
		if node.else_:
			self.dispatch(node.else_)

	def visitGlobal(self, node):
		print "Visiting a Global node"
		for n in node.getChildNodes():
			self.dispatch(n)

	#Importing
	def visitImport(self, node):
		for (full, alias) in node.names:
			self.modules.append(alias if alias else full)
			self.deps.append(full)
			
	def visitFrom(self, node):
		self.deps.append(node.modname)
		m = node.modname.split('.')[-1]#replace('.', '_')
		for (full, alias) in node.names:
			if alias:
				self.out.write("%s_%s = %s_%s" % (m, alias, m, full)) 
			self.imports[alias if alias else full] = m
			
	def visitModule(self, node):
		for n in node.getChildNodes():
			self.dispatch(n)

	def visitName(self, node, assName=None):
		if node.name in ["True", "False"]:
			self.out.write(node.name.lower())
			return
		if node.name == "self":
			self.out.write("this")
			return
		# if node.name[0] in capitals:
		# 	self.out.write("new ")
		if node.name in self.classes or node.name in self.functions or node.name in self.vars:
			self.out.write(self.module.replace(".", "_") + "_")
		if node.name in self.imports:
			self.out.write(self.imports[node.name] + "_")
		self.out.write(node.name)


	def visitConst(self, node, assName=None):
		if isinstance(node.value, str):
			self.out.write('new String("%s")' % node.value)
		else:
			if not node.value:
				node.value = 0
			self.out.write("new Number(%s)" % node.value)

	def visitDict(self, node, expr=None):
		taken = self.takeVar()
		self.out.write("%s = [];\n" % taken)
		for n in node.items:
			self.out.write("%s[" % taken)
			self.dispatch(n[0])
			self.out.write("] = ")
			self.dispatch(n[1])
			self.out.write(";")
		return Name(taken)

	def visitTuple(self, node):
		self.out.write("[")
		for n in node.nodes[:-1]:
			self.dispatch(n)
			self.out.write(",")
		self.dispatch(node.nodes[-1])
		self.out.write("]")

	def visitList(self, node, assName=None):
		self.out.write("[")
		if len(node.nodes) > 0:
			for n in node.nodes[:-1]:
				self.dispatch(n)
				self.out.write(",")
			self.dispatch(node.nodes[-1])
		self.out.write("]")

	def visitListComp(self, node, assName=None):
		#print "Visiting a ListComp node %s, %s" % (node.expr, node.quals)
		self.out.write("[];\n")
		for qual in node.quals[:-1]:
			self.dispatch(qual)
		self.dispatch(node.quals[-1], node.expr, assName)
		self.out.write("}"*len(node.quals))

	def visitListCompFor(self, node, expr=None, assName=None):
		#print "Visiting a ListCompFor node %s, %s, %s" % (node.assign, node.list, node.ifs)
		taken = self.takeVar()
		self.out.write(taken + " = ")
		self.dispatch(node.list)
		self.out.write("\nfor (x in %s){\n" % taken)
		self.dispatch(node.assign)
		self.out.write(" = %s[x];\n" % taken)
		for if_ in node.ifs:
			self.dispatch(if_)
		if expr and assName:
			self.out.write(assName +".push(")
			self.dispatch(expr)
			self.out.write(");\n")
		self.out.write("}"*len(node.ifs))
		self.releaseVar(taken)
		

	def visitListCompIf(self, node):
		self.out.write("if(")
		self.dispatch(node.test)
		self.out.write("){\n")

	#Pass
	def visitPass(self, node, classPrefix=None):
		self.out.write("//no-op pass")

	#Print with no \n
	def visitPrint(self, node):
		for n in node.getChildNodes():
			self.out.write("console.log(")
			self.dispatch(n)
			self.out.write(")")
			
	#Print with \n
	def visitPrintnl(self, node):
		for n in node.getChildNodes():
			self.out.write("console.log(")
			self.dispatch(n)
			self.out.write('+"\\n")')

	#From "asdf"[1:3]		
	def visitSlice(self, node, *args):
		self.dispatch(node.expr)
		self.out.write(".slice(")
		if not node.lower:
			self.out.write("0")
		else:
			self.dispatch(node.lower)
		if node.upper:
			self.out.write(", ")
			self.dispatch(node.upper)
		self.out.write(")")
		
	#From "asdf"[1:3:4]
	def visitSliceobj(self, node, *args):
		self.out.write(".stepSlice(")
		self.dispatch(node.nodes[0])
		self.out.write(", ")
		self.dispatch(node.nodes[1])
		self.out.write(", ")
		self.dispatch(node.nodes[2])
		self.out.write(")")
		
	#Dictionary/Tuple access
	def visitSubscript(self, node, *args):
		self.dispatch(node.expr)
		if isinstance(node.subs[0], Sliceobj):
			self.dispatch(node.subs[0])
		else:
			self.out.write('[')
			self.dispatch(node.subs[0])
			self.out.write(']')
			
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

	def binOp(self, node, op):
		left, right = node.left, node.right
		self.dispatch(left)
		self.out.write(".__"+op+"__(")
		self.dispatch(right)
		self.out.write(")")

	#Arithmetic ops
	#The ** operator
	def visitPower(self, node, name=None):
		self.binOp(node, "pow")

	#The / operator	
	def visitDiv(self, node, name=None):
		self.binOp(node, "div")

	#The % operator 
	def visitMod(self, node, name=None):
		self.binOp(node, "mod")

	#The // operator
	def visitFloorDiv(self, node, name=None):
		self.binOp(node, "floordiv")

	#The * operator
	def visitMul(self, node, name=None):
		self.binOp(node, "mul")

	#The + operator
	def visitAdd(self, node, name=None):
		self.binOp(node, "add")

    #The - operator
	def visitSub(self, node, name=None):
		self.binOp(node, "sub")

	#As in a = +b
	def visitUnaryAdd(self, node, name=None):
		self.dispatch(node.expr)
		self.out.write(".__pos__()")

	#As in a = -b		
	def visitUnarySub(self, node, name=None):
		self.dispatch(node.expr)
		self.out.write(".__neg__()")

	#Bitwise ops &, |, ^, ~, << and >>
	def visitBitand(self, node, name=None):
		self.binOp(node, "and")

	def visitBitor(self, node, name=None):
		self.binOp(node, "or")

	def visitBitxor(self, node, name=None):
		self.binOp(node, "xor")

	def visitLeftShift(self, node, name=None):
		self.binOp(node, "lshift")

	def visitRightShift(self, node, name=None):
		self.binOp(node, "rshift")

	def visitInvert(self, node, name=None):
		self.dispatch(node.expr)
		self.out.write(".__inv__()")

	#Boolean ops : not, or, and	and comparison	
	def visitNot(self, node, name=None):
		self.out.write("!")
		self.dispatch(node.expr)

	def visitOr(self, node, name=None):
		for n in node.nodes[:-1]:
			self.dispatch(n)
			self.out.write("||")
		self.dispatch(node.nodes[-1])

	def visitAnd(self, node, name=None):
		for n in node.nodes[:-1]:
			self.dispatch(n)
			self.out.write("&&")
		self.dispatch(node.nodes[-1])

	def visitCompare(self, node, name=None):
		self.dispatch(node.expr)
		for op,expr in node.ops:
			self.out.write("."+self.opdict[op]+"(")
			self.dispatch(expr)
			self.out.write(")")
			
	#Not sure there's an equivalence for these in JS
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

			# function UIElement_UIElement() {
			#     if (UIElement_UIElement.prototype.hasOwnProperty("__init__")) {
			#         this.__init__(arguments);
			#     }
			# }
			# _ = UIElement_UIElement.prototype
			# // _.__init__ = function (self){
			# // console.log(new String("WHy not!")+"n")
			# // }
			# _.cock = function(){
			# 	console.log("COCK")
			# }
			# 
			# function TextBox_TextBox() {
			#     if (TextBox_TextBox.prototype.hasOwnProperty("__init__")) {
			#         TextBox_TextBox.prototype.__init__(arguments);
			#     }
			# }
			# extend(TextBox_TextBox, UIElement_UIElement)
			# 
			#  _ = TextBox_TextBox.prototype
			#  _.__init__ = function() {
			# 	this.num = 3
			#     console.log(new String("Because") + "\n")
			# }
			# 
			# 
			# function PasswordBox_PasswordBox() {
			# 	//PasswordBox_PasswordBox.superclass.apply(this, arguments)
			#     PasswordBox_PasswordBox.prototype.__init__.apply(this, arguments);
			# }
			# extend(PasswordBox_PasswordBox, TextBox_TextBox)
			# 
			#  _ = PasswordBox_PasswordBox.prototype
			#  _.__init__ = function(a, b, c) {
			# 	console.log(this)
			# 	//this.constructor.superclass.apply(this, arguments)
			# 	this.num = this.num + 5
			#     console.log(new String("I say") + "\n")
			# }
			# 
			# 
			# 
			# 
			# //ui_elem = new TextBox_TextBox()
			# // ui_elem2 = new PasswordBox_PasswordBox()
			# ui_elem3 = new PasswordBox_PasswordBox("boom","boom","pow")
			# console.log(ui_elem3.num)
			# ui_elem3.cock()
			# // ui_elem3.cock()
