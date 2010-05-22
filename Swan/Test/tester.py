from Actors.keywords import *
from Swan.db import *
from Swan.Test.honker.models import Users, Statuses

class Test(StaticActor):
	
	def birth(self):
		print "Testing starting..."
	
	def start(self):
		print Users.get(name=equals('Fred'))
		u = Users.get(name=equals('Pete'))
		print u.email
		print u.statuses
		return True