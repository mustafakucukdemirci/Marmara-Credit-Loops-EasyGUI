from PyQt5 import QtCore, QtGui, QtWidgets, Qt

#ui file made by pyqt5 designer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(301, 433)
        MainWindow.setWindowTitle("MCL PyGUI  v.0.1")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(70, 130, 171, 21))
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 120, 701, 351))
        self.label_3.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 310, 171, 41))
        self.pushButton_3.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px;\ncolor:#ebdeb1;"
"background-color: #6c7585;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(70, 360, 171, 41))
        self.pushButton_4.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px;\n"
"background-color: #6c7585;color:#ebdeb1;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(35, 0, 291, 111))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        pixmap = QtGui.QPixmap("icon.png")
        self.label_2.setPixmap(pixmap)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-170, -10, 701, 131))
        self.label.setStyleSheet("background-color: rgb(49, 103, 120);\n"
"font: 40pt \"Microsoft Tai Le\";")
        
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 160, 171, 41))
        self.pushButton.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px;\n"
"background-color:#6c7585;color:#ebdeb1;")
        self.pushButton.setObjectName("pushButton")
        
        
        
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(75, 220, 80, 20))
        self.label_4.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px; ")
        self.label_4.setObjectName("label_4")


        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(160, 220, 80, 20))
        self.comboBox_2.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px;background-color:#6c7585; ")
        self.comboBox_2.setObjectName("label_4")
        
        
        
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 260, 171, 41))
        self.pushButton_2.setStyleSheet("font: 10pt \"Comic Sans MS\";\n"
"border:0px;\n"
"background-color:  #6c7585; color:#ebdeb1;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.comboBox.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.comboBox_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

"""
import sys
app = QtWidgets.QApplication(sys.argv)
mainwindow = QtWidgets.QMainWindow()
test = Ui_MainWindow()
test.setupUi(mainwindow)
mainwindow.show()
sys.exit(app.exec_())
"""