from UIElement import UIElement

class TextBox(UIElement):
	
	def __init__(self):
		super(TextBox, self).__init__("input")
		self.element.type = "text"
		
