import types

def test(one, two):
	print one, two, three

# f = test
# print f.func_globals
# fc = f.func_code
# 
# print "co_argcount %s\n" % str(fc.co_argcount), "co_nlocals %s\n" % str(fc.co_nlocals), "co_stacksize %s\n" % str(fc.co_stacksize), "co_flags %s\n" % str(fc.co_flags), "co_code %s\n" % str(fc.co_code), "co_consts %s\n" % str(fc.co_consts), "co_names %s\n" % str(fc.co_names), "co_varnames %s\n" % str(fc.co_varnames), "co_filename %s\n" % str(fc.co_filename), "co_name %s\n" % str(fc.co_name), "co_firstlineno %s\n" % str(fc.co_firstlineno), fc.co_lnotab
# 
# mc = types.CodeType(fc.co_argcount+1, fc.co_nlocals, fc.co_stacksize, fc.co_flags, fc.co_code, fc.co_consts, tuple(), ('three',)+fc.co_varnames, fc.co_filename, fc.co_name, fc.co_firstlineno, fc.co_lnotab)
# mf = types.FunctionType(mc, f.func_globals, "myTest")
# 
test.func_globals['three'] = "four"
test('two', 'three')
# 
