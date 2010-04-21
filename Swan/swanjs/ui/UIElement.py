class UIElement(object):
	
	def __init__(self, type, **attrs):
		self.element = native("document.createElement(type)")
		self.element.proxy = self
		self.element.id = native("id_counter++")
		if(attrs):
			self.setAttributes(**attrs)
	
	def getElement(self):
		return self.element
		
	def setAttributes(self, **attrs):
		for x, y in attrs.iteritems():
			self.setAttribute(x, y)
		return self

	def setAttribute(self, name, value):
		native("this.element.setAttribute(name, value)")
		return self
	
	def setStyles(self, **styles):
		for x, y in styles.iteritems():
			self.setStyle(x, y)
		return self
	
	def setStyle(self, name, value):
		native("this.element.style[name] = value")
		return self
	
	def nextElement(self):
		return native("this.element.nextSibling.proxy")
	
	def prevElement(self):
		return native("this.element.prevSibling.proxy")