class UIElement(object):
	
	def __init__(self, type):
		self.element = native("document.createElement(type)")
		self.element.id = native("id_counter++")