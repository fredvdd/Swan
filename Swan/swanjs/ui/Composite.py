from UIElement import UIElement

class Composite(UIElement):
	
	def __init__(self):
		super(Composite, self).__init__("div")
	
	def add(self, *elems):
		asdf = True
		for elem in elems:
			self.element.appendChild(elem.element)