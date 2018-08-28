from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication

from ui_listitem import Ui_Form

class ListItem(QWidget):
    """docstring for ClassName"""
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # remove border of lineEdit
        self.ui.lineEdit.setFrame(False)



    def setPixmap(self, pixmap):
        self.ui.labelIcon.setPixmap(pixmap)

    def setTitle(self, title):
        self.ui.lineEdit.setText(title)
        self.ui.lineEdit.setCursorPosition(0)

    def setDuration(self, duration):
        print(duration)
        duration = duration/60
        duration = "{0:.2f}".format(duration).replace('.',':')
        self.ui.labelLenght.setText(duration)

    def setChecked(self, state):
        self.ui.checkBox.setChecked(state)

    def getCheckBox(self):
        return self.ui.checkBox

    def getLineEdit(self):
        return self.ui.lineEdit


