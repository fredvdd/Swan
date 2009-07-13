import copy_reg
import pickle, marshal, types

# Based on:
# http://effbot.org/librarybook/copy-reg.htm

def code_unpickler(data):
    return marshal.loads(data)

def code_pickler(code):
    return code_unpickler, (marshal.dumps(code),)

copy_reg.pickle(types.CodeType, code_pickler, code_unpickler)