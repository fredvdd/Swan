from Actors.keywords import *
from time import sleep

class MigrateTest(MobileActor):
  
  def birth(self):
    print("MT: MigrateTest")

  def ret(self, num, string):
    print("MT: Pinged" + str(num))
    #return 'Boom-' + str(num) + '!'
    sleep(0.1)
  
  def start_migrate(self):
    print("MT: Start Migrate")
    migrate_to('edge02:8000')
    
  def arrived(self):
    print "MT: I'm here"

