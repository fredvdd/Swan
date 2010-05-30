from Swan.db import Model
from Swan.db import *

class User(Model):
	name = TextField()
	email = EmailField()
	
	def test(self):
		print "This is test"
	
	def __repr__(self):
		return "User"#"Name: %s, Email:%s" % (self.name, self.email)
		

class Status(Model):
	user_id = ForeignKey('User', "statuses")
	status = TextField(140)
	timestamp = TimeField()
	
	def __repr__(self):
		return "Status"#"At %s, %s" % (self.timestamp, self.status) 

class Follow(Model):
	user_id = ForeignKey('User', "follows")
	followed_user = ForeignKey('User', "followers")
	
	def __repr__(self):
		# print "asdfasdfas"
		# print "Getting repr for Follow %s %s" % (type(self.user_id), type(self.followed_user))
		return "Follow"#"%s follows %s" % (self.user_id, self.followed_user)