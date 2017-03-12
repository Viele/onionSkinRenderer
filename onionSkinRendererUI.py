from os import path
import pymel.core as pm
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)


class onionSkinRendererUI(QtWidgets.QMainWindow):
    kUIName = "OnionSkinRendererUI"
    kListWidth = 125

    def __init__(self, parent=getMayaMainWindow()):
        super(onionSkinRendererUI, self,).__init__(parent)

        if(pm.window(self.kUIName, exists=True)):
            pm.deleteUI(self.kUIName, wnd = True)

        self.setWindowTitle("Onion Skin Renderer")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(220)
        self.createLayout()
        self.createConnections()
        self.updateFrameList()
        self.updateObjectList()
        self.resize(200,100)
        self.setObjectName(self.kUIName)
    
    def createLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()

        # frame layout
        frameLayout = QtWidgets.QHBoxLayout()

        frameListLayout = QtWidgets.QVBoxLayout()
        self.frameList = QtWidgets.QListWidget()
        self.frameList.addScrollBarWidget(QtWidgets.QScrollBar(), QtCore.Qt.AlignRight)
        self.frameList.setMaximumWidth(onionSkinRendererUI.kListWidth)
        frameListLayout.addWidget(self.frameList)

        frameInputLayout = QtWidgets.QVBoxLayout()
        self.frameInput = QtWidgets.QLineEdit()
        self.frameInput.setValidator(QtGui.QIntValidator())
        self.addFrameBtn = QtWidgets.QPushButton("Add")
        self.removeFrameBtn = QtWidgets.QPushButton("Remove")
        self.frameDisplayTypeCBox = QtWidgets.QComboBox()
        self.frameDisplayTypeCBox.addItem("Relative")
        self.frameDisplayTypeCBox.addItem("Absolute")
        frameInputLayout.addWidget(self.frameInput)
        frameInputLayout.addWidget(self.addFrameBtn)
        frameInputLayout.addWidget(self.removeFrameBtn)
        frameInputLayout.addWidget(self.frameDisplayTypeCBox)

        frameLayout.setStretchFactor(frameListLayout,1)
        frameLayout.setStretchFactor(frameInputLayout, 3)
        frameLayout.addLayout(frameListLayout)
        frameLayout.addLayout(frameInputLayout)

        # object layout
        objectLayout = QtWidgets.QHBoxLayout()

        objectListLayout = QtWidgets.QHBoxLayout()
        self.objectList = QtWidgets.QListWidget()
        self.objectList.addScrollBarWidget(QtWidgets.QScrollBar(), QtCore.Qt.AlignRight)
        self.objectList.setMaximumWidth(onionSkinRendererUI.kListWidth)
        objectLayout.addWidget(self.objectList)

        objectInputLayout = QtWidgets.QVBoxLayout()
        self.addObjectBtn = QtWidgets.QPushButton("Add Selected")
        self.removeObjectBtn = QtWidgets.QPushButton("Remove Selected")
        
        objectInputLayout.addWidget(self.addObjectBtn)
        objectInputLayout.addWidget(self.removeObjectBtn)

        objectLayout.addLayout(objectListLayout)
        objectLayout.addLayout(objectInputLayout)

        # add to main layout
        mainLayout.addLayout(frameLayout)
        mainLayout.addLayout(objectLayout)

        self.window = QtWidgets.QWidget()
        self.window.setLayout(mainLayout)
        self.setCentralWidget(self.window)


    def createConnections(self):
        self.addFrameBtn.clicked.connect(self.addFrame)
        self.addObjectBtn.clicked.connect(self.addSelectedObject)
        self.removeFrameBtn.clicked.connect(self.removeFrame)
        self.removeObjectBtn.clicked.connect(self.removeSelectedObject)
        self.frameDisplayTypeCBox.currentIndexChanged.connect(self.setRelativeFrameDisplay)

    def addFrame(self):
        try:
            frame = self.frameInput.text()
            pm.addOnionFrame(int(frame))
            self.updateFrameList()
        except:
            print "command not found"

    def removeFrame(self):
        try:
            frame = self.frameInput.text()
            pm.removeOnionFrame(int(frame))
            self.updateFrameList()
        except:
            print "command not found"

    def addSelectedObject(self):
        try:
            sel = pm.selected()
            pm.addSelectedAsOnion()
            self.updateObjectList()
        except:
            print "command not found"

    def removeSelectedObject(self):
        try:
            sel = pm.selected()
            pm.removeSelectedFromOnion()
            self.updateObjectList()
        except:
            print "command not found"

    def setRelativeFrameDisplay(self):
        try:
            pm.setRelativeOnionDisplay(self.frameDisplayTypeCBox.currentIndex() == 0)
        except:
            pass

    def updateObjectList(self):
        self.objectList.clear()
        activeObjs = pm.getOnionList(t = 0)
        if activeObjs is not None:
            for obj in activeObjs:
                self.objectList.addItem(obj)

    def updateFrameList(self):
        self.frameList.clear()
        activeFrames = pm.getOnionList(t = 1)
        if activeFrames is not None:
            for frame in activeFrames:
                sf = str(frame)
                self.frameList.addItem(str(frame))
        
                
            
if __name__ == "__main__":

    try:
        onionUi.close()
    except:
        pass

    onionUI = onionSkinRendererUI()
    onionUI.show()
