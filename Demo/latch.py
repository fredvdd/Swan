from Actors.keywords import *
from Actors.Device.timer import Sleeper

class Latch(LocalActor):
  
  MAX_PLAYERS = 3

  def birth(self):
    self.players = []

  def join_game(self, player):
    print str(player) + ' joined the latch'
    self.players.append(player)
    if len(self.players) == Latch.MAX_PLAYERS:
      for each_player in self.players:
        each_player.start_game()
      self.players = []

class Person(LocalActor):
		
  def birth(self, latch):
    latch.join_game(self)

  def start_game(self):
    print 'starting game'

class Application(LocalActor):
  
  def birth(self):
    s = Sleeper(10)
    latch = Latch()
    p1 = Person(latch)
    p2 = Person(latch)
    sync(s.sleep())
    p3 = Person(latch)

def start():
  Application()
  
if __name__ == '__main__':
  initialise(start)
