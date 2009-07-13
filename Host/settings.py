import re
import sys
from Util.Network import ipfinder
from static import log

# The port this theatre listens on for requests
local_port = 8000

# Parse any default-overiding options from the command line
if sys.platform == 'symbian_s60':
  # The gethostbyname() that works for the pc prefers to
  # return 'localhost' in s60 even if more interesting network
  # adapters are availible, instead we need to ping the manager
  # and ask them what our ip is
  network_locator_ip = ''
  network_locator_port = 7000
  network_locator_socket = network_locator_ip + ':' + str(network_locator_port)
  local_name = ipfinder.get_ip(network_locator_ip, network_locator_port - 1)
  
else:
  # The address or hostname of this theatre as presented
  # to other theatres
  import socket
  local_name = socket.gethostbyname(socket.gethostname())
  
  # The port number the network locator is listening on
  network_locator_port = 7000
  # The address of the network locator
  network_locator_socket = "%s:%s" % (local_name, network_locator_port)
    
  for arg in sys.argv:
    lp = re.search('-p(\d+)', arg)
    la = re.search('-l(.+)', arg)
    lap = re.search('-l(.+:\d+)', arg)
    if lp:
      local_port = int(lp.group(1)) 
    if lap:
      network_locator_socket = lap.group(1)
    elif la:
      network_locator_socket = "%s:%s" %  (la.group(1), network_locator_port)

print("settings", "Local address: %s:%s, network locator: %s" % 
              (local_name, local_port, network_locator_socket))