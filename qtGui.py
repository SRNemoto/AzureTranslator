import sys
from PyQt5.QtWidgets import *
from SpchTxtHandler import SpchTxtHandler as handler 


lang_list = ["English",
            "Chinese",
            "Spanish"]
lang_code_dict =     {"English": "en-US",
                    "Chinese": "zh-CN",
                    "Spanish": "es-MX"}
filename = "api_key.txt"
api_file = open(filename, "r")
api_key = api_file.readlines()
key, service_region = api_key[0].rstrip(), api_key[1].rstrip()

class GUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.handler = handler(key, service_region)

    def initUI(self):
        w, h = 750, 500
    
        self.s2s_btn = QPushButton('Speech To Speech', self)
        size = self.s2s_btn.sizeHint()
        self.s2s_btn.resize(size)
        self.s2s_btn.move(w/2 - size.width()/2, h/2)
        self.s2s_btn.clicked.connect(self.s2s_click)
        
        self.t2t_btn = QPushButton('Text To Text', self)
        size = self.t2t_btn.sizeHint()
        self.t2t_btn.resize(size)
        self.t2t_btn.move(w/2 - size.width()/2, h/2 + size.height() * 1.5)
        self.t2t_btn.clicked.connect(self.t2t_click)       
        
        self.t2s_btn = QPushButton('Text To Speech', self)
        size = self.t2s_btn.sizeHint()
        self.t2s_btn.resize(size)
        self.t2s_btn.move(w/2 - size.width()/2, h/2 - size.height() * 1.5)    
        self.t2s_btn.clicked.connect(self.t2s_click)      
  
        
        self.textin = QPlainTextEdit(self)
        size = self.textin.sizeHint()
        self.textin.move(w/40, h/2)
        self.textin.resize(size)

        self.textout = QPlainTextEdit(self)
        size = self.textout.sizeHint()
        self.textout.move(w-w/40-size.width(), h/2)
        self.textout.resize(size)
        
        self.langboxin = QComboBox(self)
        self.langboxin.addItems(lang_list)
        size = self.langboxin.sizeHint()
        self.langboxin.move(w/40, h/2 - size.height())
        self.langboxin.resize(size)
        
        self.langboxout = QComboBox(self)
        self.langboxout.addItems(lang_list)
        size = self.langboxout.sizeHint()
        self.langboxout.move(w-w/40-size.width(), h/2 - size.height())
        self.langboxout.resize(size)
        
        # self.setGeometry(300, 300, 300, 200)
        self.resize(750, 500)
        self.setWindowTitle('Azure Translate. The Superior Google Translate')
        self.show()
    
    def s2s_click(self):
        lang_code_in = lang_code_dict[self.langboxin.currentText()]
        lang_code_out = lang_code_dict[self.langboxout.currentText()]
        
        trans = self.handler.Speech2TxtTrans(lang_code_in, [lang_code_in, lang_code_out])
        keys = trans.keys()
        
        if lang_code_in == lang_code_out:
            trans_in = trans[keys[0]]
            trans_out = trans[keys[0]]
        else:
            trans_in = trans[keys[0]]
            trans_out = trans[keys[1]]
            
        self.textin.setPlainText(trans_in)
        self.textout.setPlainText(trans_out)
        self.handler.Txt2Spch(trans_out, lang_code_out)
        
    def t2s_click(self):
        self.textin.setPlainText(self.langboxin.currentText())
        self.textout.setPlainText(self.langboxout.currentText())
        
    def t2t_click(self):
        self.textin.setPlainText(self.langboxin.currentText())
        self.textout.setPlainText(self.langboxout.currentText())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ui = GUI()
    sys.exit(app.exec_())