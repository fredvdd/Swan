import hashlib

# The number of hashes produced
REDUNDANCY = 2

NODE_ID_SIZE = 4 
MAX_ID = 2**(NODE_ID_SIZE*8)
PERIOD = MAX_ID/REDUNDANCY
KEY_RANGE = range(0, REDUNDANCY)

def hash(tohash):
  hasher = hashlib.md5()
  hasher.update(tohash)
  hash = hasher.hexdigest()
  hash = hash[0:NODE_ID_SIZE*2]
  hash = eval('0x' + hash)
  return [(PERIOD * i + hash) % MAX_ID for i in KEY_RANGE]
