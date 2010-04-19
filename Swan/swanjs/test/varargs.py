def varargs(arg1, arg2, *vargs):
	print arg1, arg2,
	print len(vargs)
	for x in vargs:
		print x,
	print 


def launch():
	varargs("One", "Two", "Three", "Four")
	varargs("Five", "Six", ["Seven","Eight"])
	varargs("Nine", "Ten", *["Eleven","Twelve"])
	


if __name__ == '__main__':
	launch()

