from UIElement import UIElement
from Composite import Composite

class Label(UIElement):
	
	def __init__(self, text):
		super(Label, self).__init__("label")
		self.element.textContent = text
		
	def forInput(self, id):
		self.element.htmlFor = id
		return self
	
	def setText(self, text):
		self.element.textContent = text

class TextBox(UIElement):
	
	def __init__(self, **attrs):
		super(TextBox, self).__init__("input", **attrs)
		self.element.type = "text"
		
	def addLabelBefore(self, label):
		self.label = label.forInput(self.element.id)
		self.container.addBefore(label,self)
		return self
	
	def addLabelAfter(self, label):
		self.label = label.forInput(self.element.id)
		self.container.addAfter(label,self)
		return self
		
	def setLabelText(self, text):
		self.label.setText(text)
	
	def getLabel(self, text):
		return self.label
		
class PasswordBox(TextBox):

	def __init__(self):
		super(PasswordBox,self).__init__()
		self.element.type = "password"