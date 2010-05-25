from Swan.Test.honker.models import * 
from Swan.handlers import Handler, FileHandler

class StatusHandler(Handler):
	bindings = {
	  #'default':'^/(?P<name>.*)(/(?P<count>.*))?/?$'
	  'default':'^/(?P<name>.*)/statuses/?$'
	}
	#gets the count latest statuses for user
	def get(self, request, response, name, count=None):
		print "get %s statuses for %s" % (name, count)
		statuses = User.get(name=equals(name)).statuses
		print statuses
		response.with_status(200).with_content_type('application/json').and_content(statuses).send()
	
	#adds a new status
	def post(self, request, response, user, status):
		pass
	
	def delete(self, request, response, user, status_id):
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
	
		