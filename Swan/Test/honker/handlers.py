from Swan.handlers import Handler, FileHandler
from models import * 
from datetime import datetime

class RootHandler(FileHandler):
	root = "/files/"
	binding = "/honker/`path`"

class Statuses(Handler):
	bindings = {
	  'default':'/`name`/statuses/?`count`?/?',
	  'status' :'/`name`/status/`id`'
	}
	
	#gets the count latest statuses for user
	def get(self, name, count=None):
		user = User.get(name=equals(name))
		statuses = user.statuses[:int(count)] if count else user.statuses
		response.send(200, statuses, 'application/json')
	
	#adds a new status
	def post(self, name, body, count=None):
		if not body:
			response.send_error(412, "Need a status").send()
		else:
			statuses = User.get(name=equals(name)).statuses
			newstatus = statuses.add(status=body['status'],timestamp=datetime.now()).save()
			response.send(200, newstatus, 'application/json')
	
	def delete_status(self, name, id=None):
		print "Deleting status %s for user %s" % (name,id)
		statuses = User.get(name=equals(name)).statuses
		statuses.delete(id=id)
		response.send(204)
	
class Followers(Handler):
	bindings = {
		'default':'/`name`/following/?',
		'follower':'/`name`/follower/`follower`',
		'followers':'/`name`/followers/?',
	}
	
	#gets following for a user
	def get(self, name):
		user = User.get(name=equals(name))
		follow_relations = user.follows
		response.send(200, [fr.followed_user for fr in follow_relations], 'application/json')
		
	#follow a user
	def post(self, name):
		print "Adding a follower for %s" % name
	
	#stop following a user
	def delete_follower(self, name, follower):
		print "Deleting follower %s for user %s" % (name, follower)
	
	#users following this user
	def get_followers(self, name):
		user = User.get(name=equals(name))
		follow_relations = user.followers
		response.send(200, [fr.user_id for fr in follow_relations], 'application/json')

class Users(Handler):
	bindings = {
		'default':'/users/?',
		'user':'/user/`name`'
	}
	
	#get all users
	def get(self):
		response.send(200, User.all(), 'application/json')
		
	#add a user
	def post(self):
		response.send(200, User.create(**body), 'application/json')
		
	def get_user(self, name):
		response.send(200, User.get(name=equals(name)), 'application/json')
		
class Timelines(Handler):
	bindings = {
		'default':'/`name`/timeline'
	}
	
	def get(self, name):
		print "Get timline for %s" % name
		user = User.get(name=equals(name))
		# statuses = list()
		# for followed in user.follows:
			# statuses += followed.statuses
		statuses = reduce(lambda a, l: a+l, map(lambda f: f.followed_user.statuses, user.follows))
		print statuses
		response.send(200, statuses, 'application/json')
		
	
	
	
	
	
	
	
	
	
	
		