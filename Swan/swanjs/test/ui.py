from Swan.swanjs.ui.TextBox import TextBox, PasswordBox
from Swan.swanjs.ui.Composite import Composite

def add(elem):
	native("$bdy.appendChild(elem.element)")

def launch():
	cont = Composite()
	add(cont)
	
	elem = TextBox()
	elem2 = PasswordBox()
	#add(elem)
	#add(elem2)
	cont.add(elem, elem2)
	elem.setLabelText("Name:")
	elem2.setLabelText("Password:")
