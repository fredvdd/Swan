from Swan.Test.honker.models import * 
from Swan.handlers import Handler, FileHandler
from Swan.static import log
from datetime import datetime

class RootHandler(FileHandler):
	root = "/files/"
	binding = "/honker/`path`"

class StatusHandler(Handler):
	bindings = {
	  'default':'/`name`/statuses/?`count`?/?'
	}
	
	#gets the count latest statuses for user
	def get(self, request, response, name, count=None):
		user = User.get(name=equals(name))
		statuses = user.statuses[:int(count)] if count else user.statuses
		response.send(200, statuses, 'application/json')
	
	#adds a new status
	def post(self, request, response, name):
		body = request.get_body()
		if not body:
			response.send_error(412, "Need a status").send()
		else:
			statuses = User.get(name=equals(name)).statuses
			statuses.add(status=body['status'],timestamp=datetime.now()).save()
			response.send(204)
	
	def delete(self, request, response, user):
		body = request.get_body()
		pass
	
# class FollowerHandler(Handler):
# 	
# 	#gets following for a user
# 	def get(self, request, response, user):
# 		pass
# 		
# 	#follow a user
# 	def post(self, request, response, user):
# 		pass
# 	
# 	#stop following a user
# 	def delete(self, request, response, user):
# 		pass
# 	
# 	#users following this user
# 	def get_followers(self, request, response, user):
# 		pass
# 	
	
		