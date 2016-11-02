# coding:utf-8

from PySide import QtGui, QtCore
import maya.OpenMayaUI as OpenMayaUI
from shiboken import wrapInstance
import pymel.all as pm

import jointEffector as Effector
reload(Effector)

__version__ = '1.0.0'

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QtGui.QWidget )

class MainWindow(QtGui.QDialog):
    
    def __init__(self, parent=getMayaWindow()):
        super(MainWindow, self).__init__(parent)

        self.initUI()
        self.connections()
        
    def initUI(self):
        self.setWindowTitle('Joint Effector')
        self.mainLayoyt = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayoyt)
        
        self.name         = BaseNameWidget()
        self.start        = SelectWidget('Start')
        self.mid          = SelectWidget('Middle')
        self.end          = SelectWidget('End')
        self.installBtn = QtGui.QPushButton('Add Effector')
        
        self.mainLayoyt.addWidget(self.name)
        self.mainLayoyt.addWidget(self.start)
        self.mainLayoyt.addWidget(self.mid)
        self.mainLayoyt.addWidget(self.end)
        self.mainLayoyt.addSpacing(10)
        self.mainLayoyt.addWidget(self.installBtn)
        self.mainLayoyt.setSpacing(0)
        self.setFixedSize(300,155)
        
    def connections(self):
        self.installBtn.clicked.connect(self.install)
        
    def install(self):
        baseName = self.name.getName()
        start    = self.start.getInput()
        mid      = self.mid.getInput()
        end      = self.end.getInput()
        Effector.hingeEffector(baseName, start, mid, end)
    

class BaseNameWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BaseNameWidget, self).__init__(parent)
        
        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Base Name:')
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFixedWidth(105)
        self.lineEdit = QtGui.QLineEdit('temp')
        layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        
    def getName(self):
        return str(self.lineEdit.text())    
    
        
class SelectWidget(QtGui.QWidget):
    
    def __init__(self, btnLabel, parent=None):
        super(SelectWidget, self).__init__(parent)
        
        layout = QtGui.QHBoxLayout()
        self.lineEdit = QtGui.QLineEdit()
        self.pushButton = QtGui.QPushButton(btnLabel)
        
        layout.addWidget(self.pushButton)
        layout.addWidget(self.lineEdit)
        
        self.setLayout(layout)
        self.pushButton.clicked.connect(self.setInput)
        self.pushButton.setFixedWidth(100)
        
        layout.setContentsMargins(0,0,0,0)
        #self.setContentsMargins(0,0,0,0)
        
    def setInput(self):
        sel = pm.ls(sl=True)[0]
        self.lineEdit.setText(str(sel.name()))
    
    def getInput(self):
        objName = self.lineEdit.text()
        if pm.objExists(objName):
            return pm.PyNode(objName)
        else:
            print '{} not exists!!'.format(objName)
              
def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    win = MainWindow()
    win.show()
