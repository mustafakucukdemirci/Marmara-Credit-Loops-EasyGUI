# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self,dialog):
        
        self.dialog = dialog
        dialog.setObjectName("dialog")
        dialog.resize(460, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        """
        self.dockWidget = QtWidgets.QDockWidget(dialog)
        self.dockWidget.setGeometry(QtCore.QRect(0, 220, 461, 101))
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget.setWidget(self.dockWidgetContents)
        """
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 391, 141))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        QtCore.QMetaObject.connectSlotsByName(dialog)

        dialog.setWindowTitle("An error occurred")
        #self.dockWidget.setWindowTitle("Show Original Error Message")
        self.label.setText("An error occurred during process.")

    def processCommand(self,aa):

        
        if(str(aa) == "b''"):
            return True
        
        aa = str(aa)[2:-5]
        aa = aa.replace("\\n","\n").replace("\\r","\t")
        self.label.setText(str(aa))
        self.label.setWordWrap(True)

        self.dialog.show()
        self.dialog.exec_()
        