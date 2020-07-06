# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


import sys
import tkinter
from PyQt5.QtWidgets import *
from tkinter import ttk,filedialog
import subprocess,sys

from threading import Thread



class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(640, 480)
        self.MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 641, 471))
        self.groupBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(110, 0, 421, 301))
        self.label.setObjectName("label")
        logo = QtGui.QPixmap("./test.png")
        self.label.setPixmap(logo)
        self.label.resize(421, 301)
        self.label.setScaledContents(True)
		
		
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(170, 315, 121, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("background-color: gray;")
        
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(330, 310, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("background-color: gray;")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 390, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("background-color: gray;")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(330, 390, 121, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("background-color: gray;")
        
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 310, 121, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("background-color: gray;")
        
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
    def closeEvent(self,Event):
        subprocess.Popen("komodo-cli.exe -ac_name=MCL stop")
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Giriş yap"))
        self.pushButton_2.setText(_translate("MainWindow", "Cüzdan Yükle"))
        self.pushButton_3.setText(_translate("MainWindow", "Yedekten Yükle"))
        self.pushButton_4.setText(_translate("MainWindow", "Yeni Profil"))




