def varargs(arg1, arg2, *vargs):
	print arg1, arg2,
	print len(vargs)
	for x in vargs:
		print x,
	print 

def stdargs(arg1, arg2, arg3, arg4):
	print arg1, arg2, arg3, arg4

def launch():
	varargs("One", "Two", "Three", "Four")
	varargs("Five", "Six", ["Seven","Eight"])
	varargs("Nine", "Ten", *["Eleven","Twelve"])
	
	stdargs("One", "Two", *["Three", "Four"])
	


if __name__ == '__main__':
	launch()

