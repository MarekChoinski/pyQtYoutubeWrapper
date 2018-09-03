# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 493)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout.addWidget(self.searchLineEdit)
        self.addButton = QtWidgets.QPushButton(self.centralWidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.progressBarSingle = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBarSingle.setProperty("value", 24)
        self.progressBarSingle.setObjectName("progressBarSingle")
        self.verticalLayout.addWidget(self.progressBarSingle)
        self.progressBarMultiple = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBarMultiple.setProperty("value", 24)
        self.progressBarMultiple.setObjectName("progressBarMultiple")
        self.verticalLayout.addWidget(self.progressBarMultiple)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.checkAllButton = QtWidgets.QPushButton(self.centralWidget)
        self.checkAllButton.setObjectName("checkAllButton")
        self.horizontalLayout_5.addWidget(self.checkAllButton)
        self.cleanButton = QtWidgets.QPushButton(self.centralWidget)
        self.cleanButton.setObjectName("cleanButton")
        self.horizontalLayout_5.addWidget(self.cleanButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mp3CheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.mp3CheckBox.setObjectName("mp3CheckBox")
        self.horizontalLayout_2.addWidget(self.mp3CheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.downloadButton = QtWidgets.QPushButton(self.centralWidget)
        self.downloadButton.setObjectName("downloadButton")
        self.horizontalLayout_3.addWidget(self.downloadButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.labelInformation = QtWidgets.QLabel(self.centralWidget)
        self.labelInformation.setObjectName("labelInformation")
        self.verticalLayout.addWidget(self.labelInformation)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addButton.setText(_translate("MainWindow", "Dodaj"))
        self.checkAllButton.setText(_translate("MainWindow", "Odznacz"))
        self.cleanButton.setText(_translate("MainWindow", "Wyczyść"))
        self.mp3CheckBox.setText(_translate("MainWindow", "*.mp3"))
        self.downloadButton.setText(_translate("MainWindow", "Pobierz"))
        self.labelInformation.setText(_translate("MainWindow", "Information comes here"))

