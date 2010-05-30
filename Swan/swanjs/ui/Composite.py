from UIElement import UIElement

class Composite(UIElement):
	
	def __init__(self, elem, **attrs):
		super(Composite, self).__init__(elem, **attrs)
		self.alphaIndex = "a"
		self.childCount = 0
	
	def add(self, *elems):
		for elem in elems:
			#self.element.appendChild(elem.getElement())
			native("this.element.appendChild(elem.getElement())")
			elem.container = self
			self.childCount += 1
		return self
	
	def addAtPosition(self, newelement, position):
		elem = self.firstElement()
		while position > 0:
			elem = elem.nextElement()
			position -= 1
		if elem:
			self.addBefore(newelement,elem)
		else:
			self.add(newelement)
	
	def addBefore(self, newelement, refelement):
		native("this.element.insertBefore(newelement.element, refelement.element)")
		newelement.container = self
		self.childCount += 1
	
	def addAfter(self, newelement, refelement):
		if refelement == self.lastElement():
			self.add(newelement)
		else:
			self.addBefore(newelement, refelement.nextElement())
	
	def firstElement(self):
		return native("this.element.firstChild.proxy")
	
	def lastElement(self):
		return native("this.element.lastChild.proxy")
		
	def elementAt(self, position):
		return native("this.element.childNodes.item(position).proxy")
		
	def remove(self, elem):
		native("this.element.removeChild(elem.element)")
		self.childCount -= 1
		return self

	def removeAtPosition(self, *positions):
		r = []
		for pos in positions:
			r.push(self.elementAt(pos))
		self.remove(*r)
		
	def removeAll(self):
		native("""for(i=this.element.childElementCount;i>0;i--){
			this.element.removeChild(this.element.lastChild);
		}""")
		
	def __len__():
		return native("this.element.childNodes.length")

class Container(Composite):
	
	def __init__(self):
		super(Container, self).__init__("div")
		

class ListElement(Composite):

	def __init__(self):
		super(ListElement, self).__init__('li')

class List(Composite):

	def __init__(self):
		super(List, self).__init__('ul')
		
	def addItem(self, *content):
		e = ListElement()
		e.add(*content)
		self.add(e)
		return self

class P(UIElement):

	def __init__(self, text, **attrs):
		super(P,self).__init__('p')
		self.element.textContent = text
