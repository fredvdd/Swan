def varkwdargs(arg1, arg2, *varargs, **kwdargs):
	print arg1, arg2,
	print len(varargs)
	for x in varargs:
		print x,
	for x, y in kwdargs.iteritems():
		print x, y,
	print

def launch():
	#varkwdargs("One", "Two", "Three", "Four", five="Five", six="Six")
	varkwdargs("Nine", "Ten", *["Eleven","Twelve"], **{'thirteen':"Thirteen", 'fourteen':"Fourteen"})


if __name__ == '__main__':
	main()

