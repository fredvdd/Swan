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
		print "Getting timeline for " + self.username
		callback(self.timeline.get(self.username), layout)
		
	def getStatuses(self, layout):
		print "Getting statuses for " + self.username
		callback(self.statuses.get(self.username), layout)


class UserList(List):

	def __init__(self, control):
		super(UserList, self).__init__()
		self.setAttribute('id','ul')
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
		self.setAttribute('id','sl')
		self.controller = control
		timeline = Button("Timeline").onClick(self.controller.getTimeline, self.displayStatuses)
		statuses = Button("Statuses").onClick(self.controller.getStatuses, self.displayStatuses)
		self.addItem(timeline, statuses)

	def displayStatuses(self,ss):
		while(len(self) > 1):
			self.remove(self.lastElement())
		for s in ss:
			self.addItem(P(s.user_id.name), P(s.status),P(s.timestamp))

class StatusForm(Form):

	def __init__(self, control, statuslist):
		super(StatusForm, self).__init__('POST', '')
		self.setAttribute('id','sf')	
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

def loadInterface(login_box):
	username = login_box.elementAt(1).getValue()
	while(len(login_box) > 1):
		login_box.remove(login_box.lastElement())
	controller = ControllerActor(username)
	statuses = StatusList(controller)
	users = UserList(controller)
	statusform = StatusForm(controller, statuses)
	body.add(statusform, statuses, users)
	controller.getTimeline(statuses.displayStatuses)


def launch():
	login_box = Container().setAttribute('id', 'lb')
	user_field = TextBox().withPlaceholder("Enter your username...")
	login_button = Button('\'Login\'').onClick(loadInterface, login_box)
	body.add(login_box.add(P('Honker'), user_field, login_button))