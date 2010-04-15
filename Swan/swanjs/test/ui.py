from Swan.swanjs.ui.TextBox import TextBox
from Swan.swanjs.ui.PasswordBox import PasswordBox

def add(elem):
	native("$bdy.appendChild(elem.element)")

def launch():
	elem = TextBox()
	elem2 = PasswordBox()
	add(elem)
	add(elem2)
	elem.setLabelText("Name:")
	elem2.setLabelText("Password:")
