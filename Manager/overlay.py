from Util.Network import rpc
from bisect import bisect
import random
from hashing import *

# Bytes for id, max is 16 (MD5 hash)


class Overlay(object):
  def __init__(self):
    self.nodes = dict()
    self.id = self.gen_id()
  
  def here(self, here):
    self.here = here
    self.add(self.id, self.here)

  def get(self, id):
  
    idlist = sorted(self.nodes)
    # Chance for optimisation
    firstgreater = bisect(idlist, id)
    # Wrap around - circular overlay
    onebefore = firstgreater - 1
    if firstgreater == len(idlist):
      firstgreater = 0
      onebefore = len(idlist) - 1
      
    after = idlist[firstgreater]
    before = idlist[onebefore]
  
    diff_above = self.diff(id, after)
    diff_below = self.diff(before, id)  

    if diff_above < diff_below:
      id = idlist[firstgreater]
    else:
      id = idlist[onebefore]
    
    return (id, self.nodes[id])
  
  def get_all(self):
    return self.nodes
    
  def get_specific(self, id):
    # if id in self.nodes
    return self.nodes[id]  
  
  def populate(self, argv):
    if len(argv) > 1:
      network_locator = rpc.RPCConnector(argv[1])
      locator = network_locator.connect()
      self.add_all(locator.sendreq())
      locator.disconnect()

      for id, loc in self.nodes.iteritems():
        if loc != self.here:
          network_locator = rpc.RPCConnector(loc)
          locator = network_locator.connect()
          locator.addnode(self.id, self.here)
          locator.disconnect()
            
  def add_all(self, newnodes):
    for id, loc in newnodes.iteritems():
      self.add(id,loc)
      
  def add(self, id, location):
      self.nodes[id] = location
  
  def remove(self, id):
    if id in self.nodes:
      del self.nodes[key]
  
  def gen_id(self):
    return random.getrandbits(NODE_ID_SIZE*8)
  
  def diff(self, low, high):
  # A warp-around diff
    if low < high:
      return high - low
    else:
      return (MAX_ID - high) + low 
    



