from Swan.swanjs.ui.native import body, callback, LocalActor
from Swan.swanjs.ui.Composite import Container, List, P
from Swan.swanjs.ui.Input import Form, TextBox, Button, SubmitButton


class ControllerActor(LocalActor):

	def birth(self, username):
		print "Initialising RequestActor for " + username
		self.username = username
		self.messages = Messages()
		self.time = None

	def submit_message(self, message, success):
		print "Submitting new message"
		callback(self.messages.post(self.username, message), success)
	
	def get_messages(self, layout):
		print "Getting messages for " + self.username
		callback(self.messages.get(self.username, self.get_time()), layout)
		
	def get_time():
		return native('new Date().getTime()')

class MessageList(List):

	def __init__(self, control):
		super(MessageList, self).__init__()
		self.setAttribute('id','sl')
		self.controller = control

	def display_messages(self,msgs):
		print "Got messages " + str(msgs)
		for msg in msgs:
			self.addItem(P(msg.name),P(msg.message))
		self.controller.get_messages(self.display_messages)

class MessageForm(Form):

	def __init__(self, control):
		super(MessageForm, self).__init__('POST', '')
		self.setAttribute('id','sf')	
		self.controller = control
		self.textbox = TextBox().setAttribute("placeholder", "What's up?")
		self.add(self.textbox)
		self.onSubmit(self.submit_message)

	def submit_message(self):
		self.controller.submit_message(self.textbox.getValue(), self.sucessful, self.fail)
		return False;
	
	def sucessful(self,response):
		print "Submission successful"
		self.textbox.setValue("")
		
	def fail(self, status):
		print "Submission failed"

def loadInterface(login_box):
	username = login_box.elementAt(1).getValue()
	while(len(login_box) > 1):
		login_box.remove(login_box.lastElement())
	controller = ControllerActor(username)
	messages = MessageList(controller)
	body.add(messages, MessageForm(controller))
	controller.get_messages(messages.display_messages)

def launch():
	login_box = Container().setAttribute('id', 'lb')
	user_field = TextBox().withPlaceholder("Enter your username...")
	login_button = Button('\'Login\'').onClick(loadInterface, login_box)
	body.add(login_box.add(P('Chatter'), user_field, login_button))