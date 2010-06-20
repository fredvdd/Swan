from Swan.server import Handler, FileHandler
from models import * 
from datetime import datetime

class RootHandler(FileHandler):
	root = "/files/"
	bindings = {"default":"/blog/`path`?"}

class Posts(Handler):
	bindings = {
	  'default':'/posts/?',
	  'post' :'/post/`id`',
	  'comments':'/post/`id`/comments'
	}
	
	def get(self):#get all posts
		response.send(200, Post.all())
	
	#adds a new status
	def post(self, body):
		newpost = Post.add(title=body['title'],body=body['body'],timestamp=datetime.now()).save()
		response.send(204)
		
	def get_post(self, id):
		response.send(200, Post.get(id=equals(id)))
		
	def get_comments(self, id):
		response.send(200, Post.get(id=equals(id)).comments)
	
	def post_comments(self, id, body):
		comments = Post.get(id=equals(id))).comments
		newcomment = comments.add(name=body['name'],comment=body['comment'],timestamp=datetime.now()).save()
		response.send(204)