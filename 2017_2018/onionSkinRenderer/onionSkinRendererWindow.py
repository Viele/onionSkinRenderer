import pymel.core as pm
import os
import json
import inspect
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import onionSkinRenderer.onionSkinRendererCore as onionCore
import onionSkinRenderer.onionSkinRendererWidget as onionWidget
import onionSkinRenderer.onionSkinRendererFrameWidget as onionFrame
import onionSkinRenderer.onionSkinRendererObjectWidget as onionObject
import onionSkinRenderer.onionSkinRendererPreferences as onionPrefs


'''
2017 Version
using pyside2
'''


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)


onionUI = None
def openOnionSkinRenderer(develop = False, dockable = False):

    if develop:
        reload(onionFrame)
        reload(onionWidget)	
        reload(onionCore)
        reload(onionObject)
        reload(onionPrefs)

    #if __name__ == "__main__":
    try:
        onionUI.close()
    except:
        pass
    
    onionUI = OnionSkinRendererWindow()
    onionUI.show(dockable = dockable)
    


'''
ONION SKIN RENDERER MAIN UI
This class creates connections between UI and CORE
'''
class OnionSkinRendererWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow, onionWidget.Ui_onionSkinRenderer):

    # 
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionSkinRendererWindow, self).__init__(parent)
        # the dockable feature creates this control that needs to be deleted manually
        # otherwise it throws an error that this name already exists
        self.deleteControl('onionSkinRendererWorkspaceControl')
        
        # This registers the override in maya
        # I previously had it as plugin, but this made it impossible to get
        # the viewRenderOverrideInstance (sth to do with python namespaces i guess)
        # so i just call init myself.
        # It feels a bit hacky, but it works anyway
        onionCore.initializeOverride()

        # member variables
        self.mOnionObjectSet = set()
        self.mAbsoluteOnionSet = set()
        self.mPrefs = {}
        self.mRelativeFrameAmount = 8
        self.mToolPath = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        self.mActiveEditor = None

        # create the ui from the compiled qt designer file
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createConnections()

        self.setOnionType()

        # load settings from the settings file
        self.loadSettings()

    #
    def closeEvent(self, event):
        # when the UI is closed, deactivate the override
        self.saveSettings()
        onionCore.uninitializeOverride()
    
    # special event for the dockable feature
    def dockCloseEventTriggered(self):
        try:
            self.saveSettings()
        except:
            pass
        onionCore.uninitializeOverride()

    # code from https://gist.github.com/liorbenhorin/217bfb7e54c6f75b9b1b2b3d73a1a43a
    def deleteControl(self, control):
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)

    #
    def createConnections(self):
        self.onionObjects_add_btn.clicked.connect(self.addSelectedObjects)
        self.onionObjects_remove_btn.clicked.connect(self.removeSelectedObjects)
        self.onionObjects_clear_btn.clicked.connect(self.clearOnionObjects)

        self.toggleRenderer_btn.clicked.connect(self.toggleRenderer)
        self.globalOpacity_slider.sliderMoved.connect(self.setGlobalOpacity)
        self.onionType_cBox.currentTextChanged.connect(self.setOnionType)
        self.drawBehind_chkBx.stateChanged.connect(self.setDrawBehind)

        self.relative_futureTint_btn.clicked.connect(self.pickColor)
        self.relative_pastTint_btn.clicked.connect(self.pickColor)
        self.relative_tint_strength_slider.sliderMoved.connect(self.setRelativeTintStrength)
        self.relative_keyframes_chkbx.clicked.connect(self.toggleRelativeKeyframeDisplay)
        self.relative_step_spinBox.valueChanged.connect(self.setRelativeStep)

        self.absolute_tint_btn.clicked.connect(self.pickColor)
        self.absolute_addCrnt_btn.clicked.connect(self.addAbsoluteFrame)
        self.absolute_add_btn.clicked.connect(self.addAbsoluteFrameFromSpinbox)
        self.absolute_tint_strength_slider.sliderMoved.connect(self.setAbsoluteTintStrength)
        self.absolute_clear_btn.clicked.connect(self.clearAbsoluteFrames)

        self.settings_clearBuffer.triggered.connect(self.clearBuffer)
        self.settings_autoClearBuffer.triggered.connect(self.setAutoClearBuffer)
        self.settings_preferences.triggered.connect(self.changePrefs)


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
        activeFrames = []
        # clear the frame of all widgets first
        for child in self.relative_frame.findChildren(OnionListFrame):
            if child.frame_visibility_btn.isChecked():
                activeFrames.append(int(child.frame_number.text()))
            child.setParent(None)
        
        # fill the relative frames list
        for index in range(self.mRelativeFrameAmount + 1):
            if not index-self.mRelativeFrameAmount/2 == 0:
                listWidget = OnionListFrame()
                frame = index-self.mRelativeFrameAmount/2
                listWidget.frame_number.setText(str(frame))
                listWidget.frame_opacity_slider.setValue(75/abs(index-self.mRelativeFrameAmount/2))
                listWidget.frame_visibility_btn.clicked.connect(self.toggleRelativeFrame)
                if frame in activeFrames: 
                    listWidget.frame_visibility_btn.setChecked(True)
                    activeFrames.remove(frame)
                listWidget.frame_opacity_slider.sliderMoved.connect(self.setRelativeOpacity)
                self.relative_frame_layout.addWidget(listWidget)
        
        for frame in activeFrames:
            onionCore.viewRenderOverrideInstance.removeRelativeOnion(frame)

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
        try:
            onionCore.viewRenderOverrideInstance.removeOnionObject(obj.fullPath())
        except:
            onionCore.viewRenderOverrideInstance.removeOnionObject(obj.nodeName())
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
        self.saveSettings()

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
        self.saveSettings()

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

    # 
    def setAutoClearBuffer(self):
        value = self.sender().isChecked()
        onionCore.viewRenderOverrideInstance.setAutoClearBuffer(value)

    #
    def changePrefs(self):
        prefUi = OnionPreferences(self)
        if prefUi.exec_():
            values = prefUi.getValues()
            onionCore.viewRenderOverrideInstance.setMaxBuffer(values['maxBuffer'])
            onionCore.viewRenderOverrideInstance.setOutlineWidth(values['outlineWidth'])
            self.mRelativeFrameAmount = values['relativeKeyCount']*2
            self.refreshRelativeFrame()
            self.saveSettings()
            
    #     
    def setRelativeStep(self):
        onionCore.viewRenderOverrideInstance.setRelativeStep(self.sender().value())
        self.saveSettings()     

    # togle active or saved editor between onion Skin Renderer and vp2
    def toggleRenderer(self):
        modelPanelList = []
        modelEditorList = pm.lsUI(editors=True)
        # find all model panels
        for myModelPanel in modelEditorList:
            if myModelPanel.find('modelPanel') != -1:
                modelPanelList.append(myModelPanel)

        onionPanel = None
        # if any of those is already set to onion skin renderer
        for modelPanel in modelPanelList:
            if pm.uitypes.ModelEditor(modelPanel).getRendererOverrideName() == 'onionSkinRenderer':
                onionPanel = pm.uitypes.ModelEditor(modelPanel)
                break

        # if there is a panel with the onion skin renderer
        # deactivate it and save the panel
        if onionPanel:
            try:
                # Always better to try in the case of active panel operations
                # as the active panel might not be a viewport.
                onionPanel.setRendererOverrideName('')
                self.mActiveEditor = onionPanel
            except Exception as e:
                # Handle exception
                print e
        else:
            # if there is a saved editor panel activate the renderer on it
            if self.mActiveEditor:
                self.mActiveEditor.setRendererOverrideName('onionSkinRenderer')
            # else toggle the active one
            else:
                for modelPanel in modelPanelList:
                    if pm.uitypes.ModelEditor(modelPanel).getActiveView():
                        try:
                            if pm.uitypes.ModelEditor(modelPanel).getRendererOverrideName() == '':
                                pm.uitypes.ModelEditor(modelPanel).setRendererOverrideName('onionSkinRenderer')
                            else:
                                pm.uitypes.ModelEditor(modelPanel).setRendererOverrideName('')
                        except Exception as e:
                            # Handle exception
                            print e   


    # 
    def setGlobalOpacity(self):
        onionCore.viewRenderOverrideInstance.setGlobalOpacity(self.sender().value())

    #
    def setOnionType(self):
        onionCore.viewRenderOverrideInstance.setOnionType(self.onionType_cBox.currentIndex())

    #
    def setDrawBehind(self):
        onionCore.viewRenderOverrideInstance.setDrawBehind(self.drawBehind_chkBx.isChecked())

            
            



    # UTILITY
    # 
    def setOnionColor(self, btn, rgba):
            btn.setStyleSheet('background-color: rgb(%s,%s,%s);'%(rgba[0], rgba[1], rgba[2]))
            onionCore.viewRenderOverrideInstance.setTint(rgba, btn.objectName())

    #
    def loadSettings(self):
        with open(os.path.join(self.mToolPath,'settings.txt')) as json_file:  
            self.mPrefs = json.load(json_file)
            self.settings_autoClearBuffer.setChecked(self.mPrefs.setdefault('autoClearBuffer',True))
            onionCore.viewRenderOverrideInstance.setAutoClearBuffer(self.mPrefs.setdefault('autoClearBuffer',True))

            self.relative_keyframes_chkbx.setChecked(self.mPrefs.setdefault('displayKeyframes',True))
            onionCore.viewRenderOverrideInstance.setRelativeKeyDisplay(self.mPrefs.setdefault('displayKeyframes',True))

            self.setOnionColor(self.relative_futureTint_btn, self.mPrefs.setdefault('rFutureTint',[0,0,125]))
            self.setOnionColor(self.relative_pastTint_btn, self.mPrefs.setdefault('rPastTint',[0,125,0]))
            self.setOnionColor(self.absolute_tint_btn, self.mPrefs.setdefault('aTint', [125,0,0]))

            self.onionType_cBox.setCurrentIndex(self.mPrefs.setdefault('onionType',1))
            self.drawBehind_chkBx.setChecked(self.mPrefs.setdefault('drawBehind', True))

            self.mRelativeFrameAmount = self.mPrefs.setdefault('relativeFrameAmount',4)
            self.refreshRelativeFrame()

            self.relative_step_spinBox.setValue(self.mPrefs.setdefault('relativeStep', 1))

            onionCore.viewRenderOverrideInstance.setMaxBuffer(self.mPrefs.setdefault('maxBufferSize', 200))
            onionCore.viewRenderOverrideInstance.setOutlineWidth(self.mPrefs.setdefault('outlineWidth',3))

    
    # save values into a json file
    def saveSettings(self):
        data = {}
        data['autoClearBuffer'] = self.settings_autoClearBuffer.isChecked()
        data['displayKeyframes'] = self.relative_keyframes_chkbx.isChecked()
        data['rFutureTint'] = self.extractRGBFromStylesheet(self.relative_futureTint_btn.styleSheet())
        data['rPastTint'] = self.extractRGBFromStylesheet(self.relative_pastTint_btn.styleSheet())
        data['aTint'] = self.extractRGBFromStylesheet(self.absolute_tint_btn.styleSheet())
        data['relativeFrameAmount'] = self.mRelativeFrameAmount
        data['relativeStep'] = self.relative_step_spinBox.value()
        data['maxBufferSize'] = onionCore.viewRenderOverrideInstance.getMaxBuffer()
        data['outlineWidth'] = onionCore.viewRenderOverrideInstance.getOutlineWidth()
        data['onionType'] = self.onionType_cBox.currentIndex()
        data['drawBehind'] = self.drawBehind_chkBx.isChecked()

        with open(os.path.join(self.mToolPath,'settings.txt'), 'w') as outfile:  
            json.dump(data, outfile)
        
    # 
    def extractRGBFromStylesheet(self, s):
        return map(int,(s[s.find("(")+1:s.find(")")]).split(','))





'''
FRAME WIDGET
the widget for displaying a frame in a list. includes visibility, opacity slider
and on demand a remove button   
'''
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
        


'''
OBJECT WIDGET
the widget for displaying an object in a list
'''
class OnionListObject(QtWidgets.QWidget, onionObject.Ui_onionSkinObject_layout):
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionListObject, self).__init__(parent)
        self.setupUi(self)



'''
Settings Dialog
in this window the user can set some preferences
'''
class OnionPreferences(QtWidgets.QDialog, onionPrefs.Ui_onionSkinRendererPreferences):
    def __init__(self, parent):
        super(OnionPreferences, self).__init__(parent)
        self.setupUi(self)
        self.relativeKeyCount_spinBox.setValue(parent.mRelativeFrameAmount/2)
        self.maxBuffer_spinBox.setValue(onionCore.viewRenderOverrideInstance.getMaxBuffer())
        self.outlineWidth_spinBox.setValue(onionCore.viewRenderOverrideInstance.getOutlineWidth())

    def getValues(self):
        values = {}
        values['maxBuffer'] = self.maxBuffer_spinBox.value()
        values['relativeKeyCount'] = self.relativeKeyCount_spinBox.value()
        values['outlineWidth'] = self.outlineWidth_spinBox.value()
        return values