# So maybe actor_id should be encapsualted,
# but storing as a string feels 'lightweight',
# portable, makes debugging that bit easier and 
# gives me serialising, hashing, comparing 
# ordering etc. for free.
# Saying that i'm sure that these high-level
# string operations are deceptively expensive.

# ...and time to write this comment < time
# to write this actor_id class.

# TODO: check out named tuple (2.6+) or c-like strucs

def generate(loc, type, num):
  #print 'g:' + loc + '-' + type + '-' + str(num)
  return loc + '-' + type + '-' + str(num)
  
def change_host(orig, loc, num):
  return generate(loc, type(orig), num)
  
def change_port(orig, port):
  return generate(ip(orig) + ':' + str(port), type(orig), num(orig))
  
def port(orig):
  return (orig.split('-')[0]).split(':')[1]

def ip(orig):
  return orig.split('-')[0].split(':')[0]

def port_from_loc(orig):
  return int(orig.split(':')[1])

def ip_from_loc(orig):
  return orig.split(':')[0]
  
def loc(orig):
  #print "o:" + orig
  return orig.split('-')[0]

def type(orig):
  return orig.split('-')[1]

def num(orig):
  return int(orig.split('-')[2])