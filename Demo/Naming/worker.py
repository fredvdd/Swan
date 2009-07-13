#  -module(worker).
#  -export([start/1]).
#  
#  start(Name) ->
#    global:register_name(Name ,self()),
#    ping_server(Name).
#  
#  ping_server(Name) ->
#    receive
#      Other ->
#        io:format("pinged"),
#        ping_server(Name)
#    end.

from Actors.keywords import *

class Worker(MobileActor):
  def birth(self):
    pass
  
  def ping(self):
    print("pinged")