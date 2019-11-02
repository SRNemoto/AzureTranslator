import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


lang_list = ["English",
			"Chinese",
			"Spanish"]
lang_code_dict = 	{"English": "en-US",
					"Chinese": "zh-CN",
					"Spanish": "es-MX"}

class GUI(QWidget):
	
	def __init__(self):
		super().__init__()
		self.initUI()
	

	def initUI(self):
		self.s2s_btn = QPushButton('Speech To Speech', self)
		self.s2s_btn.resize(self.s2s_btn.sizeHint())
		self.s2s_btn.move(50, 50)
		
		self.t2t_btn = QPushButton('Text To Text', self)
		self.t2t_btn.resize(self.t2t_btn.sizeHint())
		self.t2t_btn.move(100, 100)	   
		
		self.t2s_btn = QPushButton('Text To Speech', self)
		self.t2s_btn.resize(self.t2s_btn.sizeHint())
		self.t2s_btn.move(150, 150)	   
		
		self.textin = QLineEdit(self)
		self.textin.move(20, 20)
		self.textin.resize(self.textin.sizeHint())

		self.textout = QLineEdit(self)
		self.textout.move(20, 100)
		self.textout.resize(self.textout.sizeHint())
		
		self.langboxin = QComboBox(self)
		self.langboxin.addItems(lang_list)
		self.langboxin.move(50, 250)
		self.langboxin.resize(self.langboxin.sizeHint())
		
		self.langboxout = QComboBox(self)
		self.langboxout.addItems(lang_list)
		self.langboxout.move(50, 250)
		self.langboxout.resize(self.langboxout.sizeHint())
		
		# self.setGeometry(300, 300, 300, 200)
		self.resize(750, 500)
		self.setWindowTitle('Azure Translate. The Superior Google Translate')
		self.show()
		
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = GUI()
	sys.exit(app.exec_())