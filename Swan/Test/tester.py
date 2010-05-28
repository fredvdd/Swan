from Actors.keywords import *
from Swan.db import *
from Swan.Test.honker.models import User, Status
import pickle, datetime

class Test(StaticActor):
	
	def birth(self):
		print "Testing starting..."
	
	def start(self):
		u = User.get(name=equals('Fred'))
		statuses = u.statuses
		for status in statuses:
			print status.user_id.name
		print u.follows
		# fs = u.followers
		# print type(fs)
		# for f in u.followers:
		# 	print "Hello"
		# users = User.filter(id=greater_than(1))
		# for user in users:
		# 	print user.follows
		# print u.email
		# followers = u.followed_by
		# print type(followers)
		# for f in followers:
		# 	print f
		# c = User.create(name="Steve",email="steve@example.com")
		# print c.name
		# c.save()
		# c.email = "steve@anotherexample.com"
		# c.save()
		# print u.statuses.add(status="New status!!!",timestamp=datetime.datetime.now()).save()
		return True