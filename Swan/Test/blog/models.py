from Swan.db import Model
from Swan.db import *

class Post(Model):
	title = TextField(256)
	body = TextField(65536)
	timestamp = TimeField()

class Comment(Model):
	post_id = ForeignKey('Post', "comments")
	name = TextField(16)
	comment = TextField(65536)
	timestamp = TimeField()
	
	