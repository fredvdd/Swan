from Util.Network import rpc

vis_loc = "vector42:9001"

def func_break():
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.func_break()
  vis.disconnect()
  
func_break()