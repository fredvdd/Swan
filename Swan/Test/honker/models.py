from Swan.db import Model
from Swan.db import *

class User(Model):
	name = TextField()
	email = EmailField()
	
	def test(self):
		print "This is test"
	
	def __repr__(self):
		return "Name: %s, Email:%s, %s" % (self.name, self.email, self.__dict__)
		

class Status(Model):
	user_id = ForeignKey('User', "statuses")
	status = TextField(140)
	timestamp = TimeField()
	
	def __repr__(self):
		return "[%s] At %s, %s" % (self.user_id, self.timestamp, self.status) 

class Follow(Model):
	user_id = ForeignKey('User', "follows")
	followed_user = ForeignKey('User', "followed_by")