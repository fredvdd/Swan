class UIElement(object):
	
	def __init__(self, type):
		self.element = native("document.createElement(type)")