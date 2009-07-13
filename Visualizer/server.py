import Visualizer.displayable as svg
from Util.Network import rpc
from vislog import log
import time
import sys

def shell(vis):
  print 'Vis Running on port ' + str(port)
  execute = True
  while execute:
    if True:
      print ('..'),
      command = sys.stdin.readline().strip()
      if command == 'exit':
        execute = False
      elif command == '':
        vis.next()
      else: 
        try:
          exec(command)
        except:
          print 'command not found'


vis = svg.VisSystem()
port = 9001

valve = rpc.RPCValve(port, vis, log)
valve.listen()
shell(vis)
valve.shutdown()
time.sleep(1)
sys.exit()

