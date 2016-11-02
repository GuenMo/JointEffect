# coding:utf-8

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from shiboken import wrapInstance
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance


import maya.OpenMayaUI as OpenMayaUI
import pymel.all as pm

import jointEffector as Effector
reload(Effector)

__version__ = '1.0.0'

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)

def mayaToQtObject( inMayaUI ):
    ptr = OpenMayaUI.MQtUtil.findControl( inMayaUI )
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout( inMayaUI )
    if ptr is None:
        ptr= OpenMayaUI.MQtUtil.findMenuItem( inMayaUI )
    if ptr is not None:
        return wrapInstance( long( ptr ), QWidget )

class MainWindow(QDialog):
    
    def __init__(self, parent=getMayaWindow()):
        super(MainWindow, self).__init__(parent)

        self.initUI()
        self.connections()
        
    def initUI(self):
        self.setWindowTitle('Joint Effector')
        self.mainLayoyt = QVBoxLayout()
        self.setLayout(self.mainLayoyt)
        
        self.name         = BaseNameWidget()
        self.start        = SelectWidget('Start')
        self.mid          = SelectWidget('Middle')
        self.end          = SelectWidget('End')
        self.installBtn = QPushButton('Add Effector')
        
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
    

class BaseNameWidget(QWidget):
    def __init__(self, parent=None):
        super(BaseNameWidget, self).__init__(parent)
        
        layout = QHBoxLayout()
        label = QLabel('Base Name:')
        label.setAlignment(Qt.AlignCenter)
        label.setFixedWidth(105)
        self.lineEdit = QLineEdit('temp')
        layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        
    def getName(self):
        return str(self.lineEdit.text())    
    
        
class SelectWidget(QWidget):
    
    def __init__(self, btnLabel, parent=None):
        super(SelectWidget, self).__init__(parent)
        
        layout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.pushButton = QPushButton(btnLabel)
        
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
