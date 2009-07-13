from Util.Network import rpc

on = False

vis_loc = "vector42:9001"

def add_node(ip):
  if not on:
    return
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.add_node(ip)
  vis.disconnect()
   
def add_manager(loc):
  if not on:
    return
  print 'trying to connect'
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.add_manager(loc)
  vis.disconnect()
  print 'done'
  
def add_host(loc):
  if not on:
    return
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.add_host(loc)
  vis.disconnect()
  
def add_actor(id):
  if not on:
    return
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.add_actor(id)
  vis.disconnect()
  
  
def store_name(name, id, loc):
  if not on:
    return
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.store_name(name, id, loc)
  vis.disconnect()
  
  
def store_type(id, loc):
  if not on:
    return
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.store_type(id, loc)
  vis.disconnect()
  
