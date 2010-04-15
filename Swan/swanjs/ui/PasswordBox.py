from Swan.swanjs.ui.TextBox import TextBox

class PasswordBox(TextBox):
	
	def __init__(self):
		super(PasswordBox,self).__init__()
		self.element.type = "password"