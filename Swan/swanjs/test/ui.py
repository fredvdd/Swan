from Swan.swanjs.ui.Input import Label, TextBox, PasswordBox
from Swan.swanjs.ui.Composite import Composite
from Swan.swanjs.ui.UIElement import UIElement
from Swan.swanjs.ui.native import body

# def add(elem):
# 	native("$bdy.appendChild(elem.element)")

def launch():
	cont = Composite()
	body(cont)
	
	elem = TextBox()
	elem2 = PasswordBox().setStyle("border", "1px solid red")
	#add(elem)
	#add(elem2)
	cont.add(elem, elem2)
	elem.addLabelAfter(Label(":Name "))
	elem2.addLabelAfter(Label(":Password "))
	elem.setAttributes(value="fun", name="One")
	button = UIElement('button')
	cont.addAtPosition(button, 1)
	#cont.remove(elem, elem2)
	#cont.removeAtPosition(2,3)
	# cont.removeAll()
	print "a" >= "ab"
