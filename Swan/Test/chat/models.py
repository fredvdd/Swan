from Swan.db import Model
from Swan.db import *

class User(Model):
	name = TextField()
	email = EmailField()
		
class Flickr(Model):
	user_id = ForeignKey('User', "flickr_uid")
	uid = TextField(140)
