def kwdargs(arg1, arg2, **kwds):
	print arg1, arg2,
	for x, y in kwds.iteritems():
		print x, y,
	print

def launch():
	kwdargs("One", "Two", three="Three", four="Four")
	kwdargs("Nine", "Ten", **{'eleven':"Eleven", 'twelve':"Twelve"})
	d = {'seven':"Seven",'eight':"Eight"}
	kwdargs("Five", "Six", **d)

