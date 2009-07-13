from Actors.keywords import *
from Actors.Common.server import BServer
from ball import Ball
from time import sleep
    
class PongPlayers(NetworkSingletonActor):    
 
  def birth(self):
    self.players = []
    self.ball_location = -1
    self.ball = Ball()
    PictureInPictureManager().setball(self.ball)
    
  def add(self, player):
    self.players.append(player)
    if self.ball_location == -1:
      self.ball_location = 0
      player.incoming(self.ball) 
    self.playerchange()
      
  def leaving(self):
    if len(self.players) == 0:
      self.ball_location = -1
      self.ball.park_at(here())
      return
    self.ball_location = (self.ball_location + 1) % len(self.players)
    self.players[self.ball_location].incoming(self.ball)
    
  def current_player(self):
   if self.ball_location >= 0 and self.ball_location < len(self.players):
     return self.players[self.ball_location]
   return None
  
  def remove(self, actor):
    ball_on_dying_theatre = False
    if actor in self.players:
      if self.ball_location >= 0 and self.ball_location < len(self.players):
        ball_on_dying_theatre = self.players[self.ball_location] == actor
      self.players.remove(actor)
    if ball_on_dying_theatre:
      self.leaving()
    self.playerchange()
    
  def getall(self):
    return self.players
    
  def tellall(self, theatres):
    for player in self.players:
      player.availabletheatres(theatres)

  def actorlost(self, actor, message):
    self.remove(actor)
  
  def playerchange(self):
    PictureInPictureManager().players_are(self.players)
  
  def theatreclosing(self):
    migrate_or_die()
    
class PongTheatres(NetworkSingletonActor):
  
  def birth(self):
    self.players = PongPlayers()
    self.theatres = []
    
  def get(self):
    return self.theatres
    
  def add(self, theatre):
    self.theatres.append(theatre)
    self.players.tellall(self.theatres)
    
  def remove(self, theatre):
    if theatre in self.theatres:
      self.theatres.remove(theatre)
      self.players.tellall(self.theatres)
      
  def theatreclosing(self):
    migrate_or_die()
    
class PictureInPictureManager(BServer):
  
  def birth(self):
    BServer.birth(self)
    self.players = []
    self.batpositions = dict()
    self.playerserver = PongPlayers()
  
  def broadcast(self):
    (xpc, ypc) = self.ball.getpc()
    current_player =  self.playerserver.current_player()
    
    for player in self.players:
      callback('bat_at', player.getbatpc())
    
    for child in self.children:
      child.ball_at(current_player, xpc, ypc)
      child.bats_at(self.batpositions.values())
    sleep(0.5)
    schedule('broadcast')
    
  def bat_at(self, (player, ypc)):
    self.batpositions[player] = (player, ypc)
  
  def setball(self, ball):
    self.ball = ball
    self.broadcast()
  
  def players_are(self, players):
    self.players = players
    for child in self.children:
      child.setplayers(players)
      
  def addchild(self, child):
    BServer.addchild(self, child)
    callback('players_are',  self.playerserver.getall())
      
  def removechild(self, child):
    BServer.removechild(self, child)
    if child in self.batpositions:
      del self.batpositions[child]