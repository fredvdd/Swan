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
		self.element.parentElement.insertBefore(Label(text).forInput(self.element.id).element, self.element)