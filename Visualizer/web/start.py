from Util.Network import rpc

vis_loc = "vector42:9001"

def start():
  remote_vis = rpc.RPCConnector(vis_loc)
  vis = remote_vis.connect()
  vis.start()
  vis.disconnect()
  
start()