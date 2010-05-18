from Swan.handlers import DatabaseHandler
from Swan.fields import *

class Users(DatabaseHandler):
	name = TextField()
	email = EmailField()

class Statuses(DatabaseHandler):
	user_id = ForeignKey('Users')
	status = TextField()
	timestamp = TimeField()

class Follows(DatabaseHandler):
	user_id = ForeignKey('Users')
	followed_user = ForeignKey('Users')