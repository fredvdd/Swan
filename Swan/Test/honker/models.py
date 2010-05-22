from Swan.db import Model
from Swan.db import *

class Users(Model):
	name = TextField()
	email = EmailField()
	
	def test(self):
		print "This is test"
	
	def __repr__(self):
		return "Name: %s, Email:%s" % (self.name, self.email)
		

class Statuses(Model):
	user_id = ForeignKey('Users', "statuses")
	status = TextField(140)
	timestamp = TimeField()
	
	def __repr__(self):
		return "[%s] At %s, %s" % (self.user_id, self.timestamp, self.status) 

class Follows(Model):
	user_id = ForeignKey('Users', "follows")
	followed_user = ForeignKey('Users', "followed_by")