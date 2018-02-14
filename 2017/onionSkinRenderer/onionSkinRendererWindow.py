import pymel.core as pm
import os
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import onionSkinRenderer.onionSkinRendererCore as onionCore
import onionSkinRenderer.onionSkinRendererWidget as onionWidget
import onionSkinRenderer.onionSkinRendererFrameWidget as onionFrame
import onionSkinRenderer.onionSkinRendererObjectWidget as onionObject


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)

onionUI = None

# -----------------------------
# ONION SKIN RENDERER MAIN UI
# This class creates connections between UI and CORE
# -----------------------------
class OnionSkinRendererWindow(QtWidgets.QMainWindow, onionWidget.Ui_onionSkinRenderer):

    # 
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionSkinRendererWindow, self).__init__(parent)
        
        # This registers the override in maya
        # I previously had it as plugin, but this made it impossible to get
        # the viewRenderOverrideInstance (sth to do with python namespaces i guess)
        # so i just call init myself.
        # It feels a bit hacky, but it works anyway
        onionCore.initializeOverride()

        # member variables
        self.mOnionObjectSet = set()
        self.mAbsoluteOnionSet = set()
        # TODO let the user set the amount of relative onions with a prefs file
        self.mRelativeFrameAmount = 8

        # create the ui from the compiled qt designer file
        self.setupUi(self)

        # create the clear buffer button
        self.onionFrames_clearBuffer_btn = QtWidgets.QPushButton('Clear Buffer')
        self.onionFrames_tab.setCornerWidget(self.onionFrames_clearBuffer_btn)
        self.onionFrames_clearBuffer_btn.clicked.connect(self.clearBuffer)

        # set the colors of the color picker buttons
        # TODO: specify colors in prefs file
        self.setOnionColor(self.relative_futureTint_btn, [45,255,120])
        self.setOnionColor(self.relative_pastTint_btn, [255,45,75])
        self.setOnionColor(self.absolute_tint_btn, [200,200,50])

        self.refreshRelativeFrame()
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createConnections()

    #
    def closeEvent(self, event):
        # when the UI is closed, deactivate the override
        onionCore.uninitializeOverride()

    #
    def createConnections(self):
        self.onionObjects_add_btn.clicked.connect(self.addSelectedObjects)
        self.onionObjects_remove_btn.clicked.connect(self.removeSelectedObjects)
        self.onionObjects_clear_btn.clicked.connect(self.clearOnionObjects)

        self.relative_futureTint_btn.clicked.connect(self.pickColor)
        self.relative_pastTint_btn.clicked.connect(self.pickColor)
        self.relative_tint_strength_slider.sliderMoved.connect(self.setRelativeTintStrength)
        self.relative_keyframes_chkbx.clicked.connect(self.toggleRelativeKeyframeDisplay)

        self.absolute_tint_btn.clicked.connect(self.pickColor)
        self.absolute_addCrnt_btn.clicked.connect(self.addAbsoluteFrame)
        self.absolute_add_btn.clicked.connect(self.addAbsoluteFrameFromSpinbox)
        self.absolute_tint_strength_slider.sliderMoved.connect(self.setAbsoluteTintStrength)
        self.absolute_clear_btn.clicked.connect(self.clearAbsoluteFrames)


    # ------------------
    # UI REFRESH

    # 
    def refreshObjectList(self):
        self.onionObjects_list.clear()
        for obj in self.mOnionObjectSet:
            listWidget = OnionListObject()
            listWidget.object_label.setText(obj.nodeName())
            listWidget.object_remove_btn.clicked.connect(lambda b_obj = obj: self.removeOnionObject(b_obj))
            listItem = QtWidgets.QListWidgetItem()
            listItem.setSizeHint(listWidget.sizeHint())
            self.onionObjects_list.addItem(listItem)
            self.onionObjects_list.setItemWidget(listItem, listWidget)

    # 
    def refreshRelativeFrame(self):
        # clear the frame of all widgets first
        for child in self.relative_frame.findChildren(QtWidgets.QWidget):
            child.setParent(None)
        # fill the relative frames list
        
        for index in range(self.mRelativeFrameAmount + 1):
            if not index-self.mRelativeFrameAmount/2 == 0:
                listWidget = OnionListFrame()
                listWidget.frame_number.setText(str(index-self.mRelativeFrameAmount/2))
                listWidget.frame_opacity_slider.setValue(75/abs(index-self.mRelativeFrameAmount/2))
                listWidget.frame_visibility_btn.clicked.connect(self.toggleRelativeFrame)
                listWidget.frame_opacity_slider.sliderMoved.connect(self.setRelativeOpacity)
                self.relative_frame_layout.addWidget(listWidget)

    # 
    def refreshAbsoluteList(self):
        # remove any entries that don't exist anymore
        framesInList = []
        for i in reversed(xrange(self.absolute_list.count())):
            frame = self.absolute_list.item(i).data(QtCore.Qt.UserRole)
            framesInList.append(frame)
            if frame not in self.mAbsoluteOnionSet:
                self.absolute_list.takeItem(i)
        
        # add any missing entry
        for frame in self.mAbsoluteOnionSet:
            if frame not in framesInList:
                listWidget = OnionListFrame()
                listWidget.frame_number.setText(str(int(frame)))
                listWidget.frame_opacity_slider.setValue(onionCore.viewRenderOverrideInstance.getAbsoluteOpacity(int(frame)))
                listWidget.addRemoveButton()
                listWidget.frame_visibility_btn.setChecked(onionCore.viewRenderOverrideInstance.absoluteOnionExists(int(frame)))
                listWidget.frame_remove_btn.clicked.connect(lambda b_frame = frame: self.removeAbsoluteFrame(b_frame))
                listWidget.frame_visibility_btn.clicked.connect(self.toggleAbsoluteFrame)
                listWidget.frame_opacity_slider.sliderMoved.connect(self.setAbsoluteOpacity)
                listItem = QtWidgets.QListWidgetItem()
                listItem.setData(QtCore.Qt.UserRole, int(frame))
                listItem.setSizeHint(listWidget.sizeHint())
                # insert item at correct position
                correctRow = 0
                for i in xrange(self.absolute_list.count()):
                    if frame < self.absolute_list.item(i).data(QtCore.Qt.UserRole):
                        break
                    correctRow = i+1
                
                self.absolute_list.insertItem(correctRow, listItem)
                self.absolute_list.setItemWidget(listItem, listWidget)




    # ---------------------------
    # CONNECTIONS

    # 
    def addSelectedObjects(self):
        onionCore.viewRenderOverrideInstance.addSelectedOnion()
        for obj in pm.selected():
            self.mOnionObjectSet.add(obj)
        self.refreshObjectList()
    
    # 
    def removeSelectedObjects(self):
        onionCore.viewRenderOverrideInstance.removeSelectedOnion()
        for obj in pm.selected():
            if obj in self.mOnionObjectSet:
                self.mOnionObjectSet.remove(obj)
        self.refreshObjectList()

    #
    def removeOnionObject(self, obj):
        onionCore.viewRenderOverrideInstance.removeOnionObject(obj.fullPath())
        self.mOnionObjectSet.remove(obj)
        self.refreshObjectList()

    #
    def clearOnionObjects(self):
        onionCore.viewRenderOverrideInstance.clearOnionObjects()
        self.mOnionObjectSet.clear()
        self.refreshObjectList()

    # 
    def toggleRelativeFrame(self):
        sender = self.sender()
        frame = sender.parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        sliderValue = sender.parent().findChild(QtWidgets.QSlider, 'frame_opacity_slider').value()
        if sender.isChecked():
            onionCore.viewRenderOverrideInstance.addRelativeOnion(frame, sliderValue)
        else:
            onionCore.viewRenderOverrideInstance.removeRelativeOnion(frame)

    #
    def toggleRelativeKeyframeDisplay(self):
        sender = self.sender()
        onionCore.viewRenderOverrideInstance.setRelativeKeyDisplay(self.sender().isChecked())

        
        futureKeys = []
        pastKeys = []

        nextKey = pm.findKeyframe(ts=True, w="next")
        pastKey = pm.findKeyframe(ts=True, w="previous")

        # add next keys to list
        bufferKey = pm.getCurrentTime()
        for i in range(self.mRelativeFrameAmount/2):
            if nextKey <= bufferKey:
                break
            futureKeys.append(nextKey)
            bufferKey = nextKey
            nextKey = pm.findKeyframe(t=bufferKey, ts=True, w="next")

        # add prev keys to list
        bufferKey = pm.getCurrentTime()
        for i in range(self.mRelativeFrameAmount/2):
            if pastKey >= bufferKey:
                break
            pastKeys.append(pastKey)
            bufferKey = pastKey
            pastKey = pm.findKeyframe(t=bufferKey, ts=True, w="previous")



    # 
    def addAbsoluteFrame(self, **kwargs):
        frame = kwargs.setdefault('frame', pm.animation.getCurrentTime())
        if int(frame) not in self.mAbsoluteOnionSet:
            onionCore.viewRenderOverrideInstance.addAbsoluteOnion(frame, 50)
            self.mAbsoluteOnionSet.add(frame)
            self.refreshAbsoluteList()

    #
    def addAbsoluteFrameFromSpinbox(self):
        frame = self.sender().parent().findChild(QtWidgets.QSpinBox, 'absolute_add_spinBox').value()
        self.addAbsoluteFrame(frame = frame)

    #
    def toggleAbsoluteFrame(self):
        sender = self.sender()
        frame = sender.parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        sliderValue = sender.parent().findChild(QtWidgets.QSlider, 'frame_opacity_slider').value()
        if sender.isChecked():
            onionCore.viewRenderOverrideInstance.addAbsoluteOnion(frame, sliderValue)
        else:
            onionCore.viewRenderOverrideInstance.removeAbsoluteOnion(frame)
    
    #
    def removeAbsoluteFrame(self, frame):
        onionCore.viewRenderOverrideInstance.removeAbsoluteOnion(frame)
        self.mAbsoluteOnionSet.remove(frame)
        self.refreshAbsoluteList()

    #
    def clearAbsoluteFrames(self):
        onionCore.viewRenderOverrideInstance.clearAbsoluteOnions()
        self.mAbsoluteOnionSet.clear()
        self.refreshAbsoluteList()

    # 
    def clearBuffer(self):
        onionCore.viewRenderOverrideInstance.rotOnions()

    # 
    def pickColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.setOnionColor(self.sender(), color.getRgb())

    #
    def setRelativeOpacity(self):
        opacity = self.sender().value()
        frame = self.sender().parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        onionCore.viewRenderOverrideInstance.setRelativeOpacity(frame, opacity)

    #
    def setAbsoluteOpacity(self):
        opacity = self.sender().value()
        frame = self.sender().parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        onionCore.viewRenderOverrideInstance.setAbsoluteOpacity(int(frame), opacity)

    def setRelativeTintStrength(self):
        onionCore.viewRenderOverrideInstance.setRelativeTintStrength(
            self.sender().value()
        )

    def setAbsoluteTintStrength(self):
        onionCore.viewRenderOverrideInstance.setAbsoluteTintStrength(
            self.sender().value()
        )


            
            



    # UTILITY
    # 
    def setOnionColor(self, btn, rgba):
            btn.setStyleSheet('background-color: rgb(%s,%s,%s);'%(rgba[0], rgba[1], rgba[2]))
            onionCore.viewRenderOverrideInstance.setTint(rgba, btn.objectName())


# -------------------------
# FRAME WIDGET
# the widget for displaying a frame in a list. includes visibility, opacity slider
# and on demand a remove button   
class OnionListFrame(QtWidgets.QWidget, onionFrame.Ui_onionSkinFrame_layout):
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionListFrame, self).__init__(parent)
        self.setupUi(self)

    def addRemoveButton(self):
        self.frame_remove_btn = QtWidgets.QPushButton('rm')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_remove_btn.sizePolicy().hasHeightForWidth())
        self.frame_remove_btn.setSizePolicy(sizePolicy)
        self.frame_remove_btn.setMinimumSize(QtCore.QSize(16, 16))
        self.frame_remove_btn.setMaximumSize(QtCore.QSize(16, 16))
        self.frame_widget_layout.addWidget(self.frame_remove_btn)
        


# ----------------------
# OBJECT WIDGET
# the widget for displaying an object in a list
class OnionListObject(QtWidgets.QWidget, onionObject.Ui_onionSkinObject_layout):
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionListObject, self).__init__(parent)
        self.setupUi(self)