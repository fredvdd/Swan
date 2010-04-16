from UIElement import UIElement

class Label(UIElement):
	
	def __init__(self, text):
		super(Label, self).__init__("label")
		self.element.textContent = text
		return self
		
	def forInput(self, id):
		self.element.htmlFor = id
		return self

class TextBox(UIElement):
	
	def __init__(self):
		super(TextBox, self).__init__("input")
		self.element.type = "text"
		
	def setLabelText(self, text):
		label = Label(text)
		label.forInput(self.element.id)
		self.element.parentElement.insertBefore(label.element, self.element)
		
class PasswordBox(TextBox):

	def __init__(self):
		super(PasswordBox,self).__init__()
		self.element.type = "password"