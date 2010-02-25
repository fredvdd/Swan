from Util.logger import FileLogger
import re

file_loc = '/tmp/swan.log'
log = FileLogger(file_loc)

mimepattern = re.compile(r"(?P<type>[\w\*\+]+)/(?P<subtype>[\w\*\+]+)(\s*;\s*q=(?P<quality>[\d\.]+))?")

#returns an ordered list of preferred mimetypes
def parse_accept(accept):
	if not accept:
		return ["*/*"]
	types = accept.split(',')
	if len(types) < 2:  #only one type so return
		return types	#assumes no quality...
	o = [] #insertion list for types
	for tipe in types:
		match = mimepattern.match(tipe.strip())
		if match:
			parts = match.groupdict()
			if not parts['quality']:
				parts['quality'] = 1.0
			else:
				parts['quality'] = float(parts['quality'])
			p = 0
			for ordered in o:
				if order(parts, ordered):
					break;
				else:
					p += 1
			o = o[:p] + [parts] + o[p:] #do insertion
	return map(lambda i: i['type']+"/"+i['subtype'], o)

def order(one, two):
	if one['type'] == two['type']:
		if one['subtype'] == '*':
			return False
		elif two['subtype'] == '*':
			return True
		else:
			return one['quality'] > two['quality']
	else:
	 	return one['quality'] > two['quality']