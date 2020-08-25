# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'downloading.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess

class Ui_Dialog(object):
    def setLANG(self,lang):
        self.lang = lang
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 250)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(30, 180, 441, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 50, 431, 71))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(120, 150, 241, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        Dialog.setWindowTitle("fetch-params")
        self.label.setText(self.lang["initial_downloading"])
#        self.label_2.setText("Filename")

        
        
class fetchparams(QtCore.QThread):
    ssignal = QtCore.pyqtSignal(object)
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        process = subprocess.Popen("fetch-params.bat", stdout=subprocess.PIPE)
        for line in process.stdout:
            try:
                print("process poll :",process.poll())
                if(process.poll() != None):
                    break
                line = str(line)
                line = line.replace(",","")
                line = line.split(" ")
                self.ssignal.emit(line[4])
            except AttributeError:
                continue
        