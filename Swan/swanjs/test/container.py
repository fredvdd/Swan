
def launch():
	# d = {'one':'One','two':'Two'}
	# d['one'] = ('ONE','TWO') #set item
	# e = d['one'] 	#get item
	# del d['one'] 	#del item
	# print d
	# print None
	
	l = ['one','two','three']
	# l[0] = 'ONE'
	# print l[1]
	# del l[1]
	# print l
	# print l[1:2]
	# l[:1] = ['FOUR', 'FIVE']
	# del l[:1]
	# print l
	#print l[0:5:2]
	l[0:5:2] = ['FOUR','FIVE']
	print l
	del l[0:5:2]
	print l


if __name__ == '__main__':
	launch()

