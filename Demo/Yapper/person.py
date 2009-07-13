from Actors.keywords import *
from datetime import datetime
import Util.ids

class Person(NamedSingletonActor):
  def birth(self):
    self.name = None
    self.yips = list()
    self.i_follow = set()
    self.followers = set()
    self.wall = list()
   
  def attach(self, name, at):
    if self.name is None:
      self.name = name
    if ids.ip(self.actor_id) != ids.ip_from_loc(at):
      migrate_to(at)

  def follow(self, friend_name):
    friend = find_name(friend_name)
    if friend.actor_id is None:
      print("** '" + friend_name + "' is not on Yapper :-(")
    else:
      self.i_follow.add(friend)
      friend.add_follower(self.name)

  def add_follower(self, follower):
    self.followers.add(follower)    

  def yap(self, yip):
    now = datetime.now()
    hour_min = str(now.hour) + ":" + str(now.minute)
    yip = (hour_min, yip)
    self.yips.append(yip)
    self.updated('I', yip)
    for person_name in self.followers:
      person = find_name(person_name)      
      person.updated(self.name, yip)

  def updated(self, name, yip):
    self.wall.append("At " + yip[0] + " " + name + " yapped: " + yip[1])
    if len(self.wall) > 10:
      del self.wall[0:(len(self.wall) - 10)]

  def print_wall(self):
    for yip in self.wall:
      print '+ ' + yip

  def migrate_away(self):
    holder = find_type("Holder")
    theatre = ids.loc(holder.actor_id)
    migrate_to(theatre)
