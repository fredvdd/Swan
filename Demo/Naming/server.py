#  -module(server).
#  -import(worker, [ping_server/0]).
#  -import(lists, [seq/3, concat/1]).
#  -export([server/2, start/2]).
#  
#  server(Name, Num_nodes) ->
#    receive
#      {start} ->
#        Ls = seq(0, 9, 1),
#        Names = [list_to_atom(concat([a , Name, "_", L])) || L <- Ls ],
#        Pids = [spawn(worker, start, [N]) || N <- Names],
#        server(Name, Num_nodes);
#      {lookup} ->
#        Ls = seq(1, Num_nodes, 1),
#        Names = [list_to_atom(concat([a , L, "_", (L rem Num_nodes)])) || L <- Ls ],    
#        Pids = [global:whereis_name(N) || N <- Names],
#        [P ! ping || P <- Pids],
#        server(Name, Num_nodes);
#      Other ->
#        io:format("stuck"),
#        server(Name, Num_nodes)
#    end.
#  
#  start(Name, Num_nodes) ->
#    A = spawn(server, server, [Name, Num_nodes]),
#    A ! {start},
#    timer:sleep(15000),
#    A ! {lookup}.
# 
import time
import sys

from Actors.keywords import *
from Demo.Naming.worker import Worker

class Server(MobileActor):
  def birth(self, my_name, num_nodes):
    ls = range(0, 10)
    store_names = [str(my_name) + "_" + str(l) for l in ls]
    [name(n, Worker()) for n in store_names]
    
    time.sleep(15)
    
    ns = range(1, num_nodes + 1)
    lookup_names = [str(n) + "_" + str(n % num_nodes) for n in ns]
    actors = [find_name(n) for n in lookup_names]
    [a.ping() for a in actors]
    
def start():
  Server(int(sys.argv[1]), int(sys.argv[2]))

if __name__ == '__main__':  
  initialise(start)