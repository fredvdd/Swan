from Swan.swanjs.ui.native import body, callback, LocalActor
from Swan.swanjs.ui.Composite import Container, List, P
from Swan.swanjs.ui.Input import Form, TextBox, Button, SubmitButton
from Swan.swanjs.ui.UIElement import UIElement


class ControllerActor(LocalActor):

	def birth(self, username):
		self.username = username
		self.messages = Messages()
		self.photos = Photos()
		self.time = None

	def submit_message(self, message, success):
		callback(self.messages.post(self.username, message), success)

	def submit_photo(self,title,success):
		callback(self.photos.get_photo(self.username,title), success)
	
	def get_messages(self, layout):
		callback(self.messages.get(self.username, self.get_time()), layout)
		
	def get_time():
		return native('new Date().getTime()')

class MessageList(List):

	def __init__(self, control):
		super(MessageList, self).__init__()
		self.controller = control

	def display_messages(self,msgs):
		for msg in msgs:
			if(msg.type == 'photo'):
				self.addPhoto(msg)
			else:
				self.addItem(P(msg.name),P(msg.message))
		self.controller.get_messages(self.display_messages)
	
	def addPhoto(self, p):
		url = "http://farm"+p.farm+".static.flickr.com/"+p.server+"/"+p.id+"_"+p.secret+".jpg"
		self.addItem(P(p.user),UIElement('img').setAttribute('src',url))

class MessageForm(Form):

	def __init__(self, control):
		super(MessageForm, self).__init__('POST', '')
		self.controller = control
		self.textbox = TextBox()
		self.add(self.textbox)
		self.onSubmit(self.submit_message)

	def submit_message(self):
		msg = self.textbox.getValue()
		if msg.startswith("photo "):
			self.controller.submit_photo(msg[6:], self.successful, self.fail)
		else:
			self.controller.submit_message(msg, self.successful, self.fail)
	
	def successful(self,response):
		print "Submission successful"
		self.textbox.setValue("")
		
	def fail(self, status):
		print "Submission failed"

def loadInterface():
	username = body.firstElement().getValue()
	body.removeAll()
	#while(len(body) > 1):
	#	body.remove(body.lastElement())
	controller = ControllerActor(username)
	messages = MessageList(controller)
	body.add(messages, MessageForm(controller))
	controller.get_messages(messages.display_messages)

def launch():
	body.add(TextBox().withPlaceholder("Enter your username..."), Button('start').onClick(loadInterface))
