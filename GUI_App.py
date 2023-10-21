from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
import sys

class Ui_Form(object):
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(630, 700)
        Form.setWindowTitle("Applikazija za racunanje potrosnje elektricne energije")
        
        
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(25, 60, 485, 50))
        self.label.setStyleSheet("color:red; font-size:20px")
        self.label.setText("Uvoz podataka\n____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
        
        # dugme za odabir csw fajla
        self.pushButton1 = QtWidgets.QPushButton(Form)
        self.pushButton1.setGeometry(QtCore.QRect(25, 120, 150, 50))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setStyleSheet("background-color:orange")
        
        # text box za prikaz odabranog .xlsx fajla
        self.textBox1 = QtWidgets.QTextBrowser(Form)
        self.textBox1.setGeometry(QtCore.QRect(195, 120, 150, 50))
        self.textBox1.setObjectName("textBox1")
        
        # dugme da pokrene upis u bazu 
        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(365, 120, 150, 50))
        self.pushButton2.setObjectName("pushButton2")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Applikazija za racunanje potrosnje elektricne energije"))    
        
        self.pushButton1.setText(_translate("Form", "Ucitaj .xlsx podatke"))
        self.pushButton1.clicked.connect(self.pushButton_handler1)
        
        self.pushButton2.setText(_translate("Form", "Upisi podatke u bazu"))
        self.pushButton2.clicked.connect(self.pushButton_handler2)
        
    def pushButton_handler1(self):
        print("Dugme za odabir .xlsx podataka pritisnut")
        try:
            self.open_dialog_box1()
        except:
            print("Greska prilikom odabira .xlsx podataka")
            
    def pushButton_handler2(self):
        print("Dugme za upis podataka u bazu pritisnut")


    def open_dialog_box1(self):
        print("Otvaram .xlsx fajl ...")
        try:
            #filename = QFileDialog.getOpenFileName(directory="Desktop\IIS_2022-2023", filter = "xslx(*.xsls)")
            filename = QFileDialog.getOpenFileName()
            path = filename[0]
            print(path)
            xlsx_data = path.split('/')[5]
            self.textBox1.setText(path.split('/')[5])
            
            with open(path, "r") as f:
                print(f.readline())
        except:
            print("Greska prilikom odabira .xlsx podataka")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

