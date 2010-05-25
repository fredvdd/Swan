from Actors.keywords import *
from Swan.db import *
from Swan.Test.honker.models import User, Status
import pickle, datetime

class Test(StaticActor):
	
	def birth(self):
		print "Testing starting..."
	
	def start(self):
		print User.get(name=equals('Fred'))
		u = User.get(name=equals('Fred'))
		print u.email
		followers = u.followed_by
		print type(followers)
		for f in followers:
			print f
		# c = User.create(name="Steve",email="steve@example.com")
		# print c.name
		# c.save()
		# c.email = "steve@anotherexample.com"
		# c.save()
		# print u.statuses.add(status="New status!!!",timestamp=datetime.datetime.now()).save()
		return True