from Actors.keywords import *
from time import sleep

class MigrateTest(MobileActor):
  def birth(self):
    print("MT: MigrateTest")
    self.pinger = find_type("Pinger")

  def ret(self, num, string):
    print("MT: Pinged" + str(num))
    self.pinger.pong(self.actor_id)
    #return 'Boom-' + str(num) + '!'
  
  
  def start_migrate(self):
    print("MT: Start Migrate")
    migrate_to('edge03:8000')
    
  def arrived(self):
    print "MT: I'm here"
