from Util.Network import rpc

vis_loc = "vector42:9001"

def step():
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.step()
  vis.disconnect()
  
step()