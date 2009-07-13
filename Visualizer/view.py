import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import *


class Stepper(QDialog): 
  def __init__(self, parent=None):
    super(Stepper, self).__init__(parent) 
    self.text = QLineEdit("Hello World") 
    layout = QVBoxLayout() 
    layout.addWidget(self.text) 
    self.setLayout(layout) 
    self.setWindowTitle("Stage Stepper") 
    


app = QApplication(sys.argv)
stepper = Stepper() 
stepper.show() 
app.exec_()