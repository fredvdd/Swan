from UIElement import UIElement
from Composite import Composite

class Form(Composite):
	
	def __init__(self, method, action, *elems, **attrs):
		super(Form, self).__init__('form', **attrs)
		self.setAttribute('method', method)
		self.setAttribute('action', action)
		self.add(*elems)
		def submit_func():
			return self.proxy.onsubmit()
		self.element.onsubmit = submit_func
	
	def onSubmit(self, func):
		self.onsubmit = func
		return self

class Label(UIElement):
	
	def __init__(self, text):
		super(Label, self).__init__("label")
		self.element.textContent = text
		
	def forInput(self, id):
		self.element.htmlFor = id
		return self
	
	def setText(self, text):
		self.element.textContent = text

class Input(UIElement):
	
	def __init__(self, **attrs):
		super(Input, self).__init__("input", **attrs)
		
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
	
	def withPlaceholder(self, text):
		self.setAttribute('placeholder', text)
		return self
	
	def getLabel(self, text):
		return self.label
		
	def getValue(self):
		return self.element.value;
	
	def setValue(self, newval):
		self.element.value = newval
		return self

class TextBox(Input):
		
	def __init__(self):
		super(TextBox,self).__init__()
		self.element.type = "text"	
		
class PasswordBox(TextBox):

	def __init__(self):
		super(PasswordBox,self).__init__()
		self.element.type = "password"
		
class Button(Input):
	
	def __init__(self, text):
		super(Button,self).__init__()
		self.element.type = "button"
		self.element.value = text
		def click_func():
			if self.proxy.onclick:
				return self.proxy.onclick.call(self.proxy.onclick.__self__, self.proxy.onclick_args)
		self.element.onclick = click_func
		self.onclick_args = None
		self.onclick = None
	
	def onClick(self, func, args):
		self.onclick_args = args
		self.onclick = func
		return self
		
class SubmitButton(Button):

	def __init__(self, text):
		super(SubmitButton,self).__init__(text)
		self.element.type = "submit"

class TextArea(Input):
	
	def __init__(self, text, **attrs):
		self.element = UIElement('textarea', **attrs).element
		self.element.proxy = self
		if text:
			self.element.value = text
		