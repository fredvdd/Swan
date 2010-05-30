from Swan.swanjs.ui.native import body, callback, LocalActor
from Swan.swanjs.ui.Composite import Container, List, P
from Swan.swanjs.ui.Input import Form, TextBox, TextArea, Button, SubmitButton
		
class ControllerActor(LocalActor):

	def birth(self, username):
		print "Initialising RequestActor for " + username
		self.username = username
		self.timeline = Timelines()
		self.followers = Followers()
		self.statuses = Statuses()
		self.users = Users()

	def submit_status(self, status, success, failure):
		print "Submitting new status"
		callback(self.statuses.post(self.username, status), success, failure)

	def loadFollowers(self, layout):
		print "Loading followers for " + self.username
		callback(self.followers.get_followers(self.username), layout)

	def loadFollowing(self, layout):
		print "Loading followers for " + self.username
		callback(self.followers.get(self.username), layout)

	def loadUsers(self, layout):
		print "Loading all users"
		callback(self.users.get(), layout)
		
	def getTimeline(self, layout):
		print "Getting timeline"
		callback(self.timeline.get(self.username), layout)
		
	def getStatuses(self, layout):
		print "Getting statuses"
		callback(self.statuses.get(self.username), layout)


class UserList(List):

	def __init__(self, control):
		super(UserList, self).__init__()
		self.controller = control
		followers = Button("Followers").onClick(self.controller.loadFollowers, self.displayUsers)
		following = Button("Following").onClick(self.controller.loadFollowing, self.displayUsers)
		allusers  = Button("All").onClick(self.controller.loadUsers, self.displayUsers)
		self.addItem(followers, following, allusers)

	def displayUsers(self,fs):
		while(len(self) > 1):
			self.remove(self.lastElement())
		for f in fs:
			self.addItem(P(f.name),P(f.email))
			
class StatusList(List):

	def __init__(self, control):
		super(UserList, self).__init__()
		self.controller = control
		timeline = Button("Timeline").onClick(self.controller.getTimeline, self.displayStatuses)
		statuses = Button("Statuses").onClick(self.controller.getStatuses, self.displayStatuses)
		self.addItem(timeline, statuses)

	def displayStatuses(self,ss):
		while(len(self) > 1):
			self.remove(self.lastElement())
		for s in ss:
			self.addItem(P(s.status),P(s.timestamp))

class StatusForm(Form):

	def __init__(self, control, statuslist):
		super(StatusForm, self).__init__('POST', '')	
		self.controller = control
		self.statuslist = statuslist
		self.textarea = TextArea().setAttribute("placeholder", "What's up?")
		self.submit = SubmitButton("Honk!")
		self.add(self.textarea, self.submit)
		self.onSubmit(self.submit_status)

	def submit_status(self):
		self.controller.submit_status(self.textarea.getValue(), self.sucessful, self.fail)
		return False;
	
	def sucessful(self,response):
		print "Submission successful"
		self.textarea.setValue("")
		
	def fail(self, status):
		print "Submission failed"

def loadInterface(user_field):
	body.removeAll()
	username = user_field.getValue()
	controller = ControllerActor(username)
	statuses = StatusList(controller).setAttribute("style","border:1px solid red")
	users = UserList(controller).setAttribute("style","border:1px solid blue")
	statusform = StatusForm(controller, statuses)
	body.add(statuses, statusform, users)


def launch():
	user_field = TextBox().withPlaceholder("Enter your username...")
	login_button = Button('\'Login\'').onClick(loadInterface, user_field)
	body.add(user_field, login_button)