from Swan.swanjs.ui.native import body, LocalActor
from Swan.swanjs.ui.Composite import Container, List
from Swan.swanjs.ui.Input import Form, TextArea, Button, SubmitButton
from handlers import *

class StatusForm(Form):
	
	def __init__(self):
		super(StatusForm, self).__init__('POST', '')	
		self.textarea = TextArea().setAttribute("placeholder", "What's up?")
		self.submit = SubmitButton("Honk!")
		self.add(self.textarea, self.submit)
		self.onSubmit(self.submit_status)
		
	def submit_status(self):
		print "Submitting status:" + self.textarea.getValue()
		return False;
		
	

class ControllerActor(LocalActor):
	
	def birth(self):
		print "Initialising RequestActor"
		
	def submit_status(self, user, status, success):

def launch():
	controller = ControllerActor()
	
	statusform = StatusForm()
	statuses = List().setAttribute("style","border:1px solid black")
	users = List().setAttribute("style","border:1px solid blue")
	
	users.addElement(Button("Followers"), Button("Following"), Button("All"))
	
	main_container = Container()
	body(main_container)
	main_container.add(statusform, statuses, users)
	print "Launched"