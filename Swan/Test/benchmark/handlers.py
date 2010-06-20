from Swan.server import Handler

class TestHandler(Handler):
	bindings = {'default':'/test/?'}
	
	def get(self):
		response.send(200, "This request was succesful", 'text/html')