import pymel.core as pm
import os
import json
import inspect
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import onionSkinRenderer.core as core
import onionSkinRenderer.wdgt_Window as wdgt_Window
import onionSkinRenderer.wdgt_Frame as wdgt_Frame
import onionSkinRenderer.wdgt_MeshListObj as wdgt_MeshListObj
import onionSkinRenderer.wdgt_Preferences as wdgt_Preferences

import onionSkinRenderer.core_clearRender as clearRender
import onionSkinRenderer.core_hudRender as hudRender
import onionSkinRenderer.core_presentTarget as presentTarget
import onionSkinRenderer.core_quadRender as quadRender
import onionSkinRenderer.core_sceneRender as sceneRender


'''
2017 and 2018 Version
using pyside2
'''

'''
Naming Conventions:
    Constants: are in caps, seperated by "_"
    Global variables: "G_" prefix
    os: abbreviation for onion skin
    osr: abbreviation for onion skin renderer
'''


DEBUG_ALL = False


# wrapper to get mayas main window
def getMayaMainWindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)



# global variable holding the instance of the window
G_onionUI = None

# convenient function to open the osr ui
def openOnionSkinRenderer(develop = False, dockable = False):

    if develop:
        reload(core)
        reload(clearRender)
        reload(hudRender)
        reload(presentTarget)
        reload(quadRender)
        reload(sceneRender)
        reload(wdgt_Frame)
        reload(wdgt_Window)	
        reload(wdgt_MeshListObj)
        reload(wdgt_Preferences)

    try:
        G_onionUI.close()
    except:
        pass
    
    G_onionUI = osrController()
    G_onionUI.show(dockable = dockable)
    


'''
ONION SKIN RENDERER MAIN UI
This class is the main ui window. It manages all user events and links to the core
'''
class osrController(MayaQWidgetDockableMixin, QtWidgets.QMainWindow, wdgt_Window.Ui_onionSkinRenderer):

    # 
    def __init__(self, parent = getMayaMainWindow()):
        super(osrController, self).__init__(parent)
        # the dockable feature creates this control that needs to be deleted manually
        # otherwise it throws an error that this name already exists
        self.deleteControl('onionSkinRendererWorkspaceControl')
        
        # This registers the override in maya
        # I previously had it as plugin, but this made it impossible to get
        # the G_osrInstance (sth to do with python namespaces i guess)
        # so i just call init myself.
        # It feels a bit hacky, but it works anyway
        core.initializeOverride()
        # member variables
        self.mwdgt_MeshListObjSet = set()
        self.mAbsoluteOnionSet = set()
        self.mPrefs = {}
        self.mRelativeFrameAmount = 8
        self.mToolPath = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        self.mActiveEditor = None

        # create the ui from the compiled qt designer file
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createConnections()

        # load settings from the settings file
        self.loadSettings()

    #
    def closeEvent(self, event):
        # when the UI is closed, deactivate the override
        if DEBUG_ALL: print 'close event start'
        self.saveSettings()
        core.uninitializeOverride()
        if DEBUG_ALL: print 'close event end'
    
    # special event for the dockable feature
    def dockCloseEventTriggered(self, event):
        if DEBUG_ALL: print 'dock close event start'
        try:
            self.saveSettings()
        except Exception as e:
            print e
        core.uninitializeOverride()
        if DEBUG_ALL: print 'dock close event end'

    # code from https://gist.github.com/liorbenhorin/217bfb7e54c6f75b9b1b2b3d73a1a43a
    def deleteControl(self, control):
        if DEBUG_ALL: print 'delete Control'
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

        self.tint_type_cBox.currentTextChanged.connect(self.setTintType)
        self.relative_futureTint_btn.clicked.connect(self.pickColor)
        self.relative_pastTint_btn.clicked.connect(self.pickColor)
        self.relative_tint_strength_slider.sliderMoved.connect(self.setTintStrength)
        self.relative_keyframes_chkbx.clicked.connect(self.toggleRelativeKeyframeDisplay)
        self.relative_step_spinBox.valueChanged.connect(self.setRelativeStep)

        self.absolute_tint_btn.clicked.connect(self.pickColor)
        self.absolute_addCrnt_btn.clicked.connect(self.addAbsoluteFrame)
        self.absolute_add_btn.clicked.connect(self.addAbsoluteFrameFromSpinbox)
        self.absolute_clear_btn.clicked.connect(self.clearAbsoluteFrames)

        self.settings_clearBuffer.triggered.connect(self.clearBuffer)
        self.settings_autoClearBuffer.triggered.connect(self.setAutoClearBuffer)
        self.settings_preferences.triggered.connect(self.changePrefs)
        self.settings_saveSettings.triggered.connect(self.saveSettings)

        self.onionObjects_grp.clicked.connect(self.toggleGroupBox)
        self.onionSkinFrames_grp.clicked.connect(self.toggleGroupBox)
        self.onionSkinSettings_grp.clicked.connect(self.toggleGroupBox)



    # ------------------
    # UI REFRESH

    # 
    def refreshObjectList(self):
        self.wdgt_MeshListObjs_list.clear()
        for obj in self.mwdgt_MeshListObjSet:
            listWidget = OnionListObject()
            listWidget.object_label.setText(obj.nodeName())
            listWidget.object_remove_btn.clicked.connect(lambda b_obj = obj: self.removewdgt_MeshListObj(b_obj))
            listItem = QtWidgets.QListWidgetItem()
            listItem.setSizeHint(listWidget.sizeHint())
            self.wdgt_MeshListObjs_list.addItem(listItem)
            self.wdgt_MeshListObjs_list.setItemWidget(listItem, listWidget)

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
                listWidget.frame_visibility_btn.toggled.connect(self.toggleRelativeFrame)
                if frame in activeFrames: 
                    listWidget.frame_visibility_btn.setChecked(True)
                    activeFrames.remove(frame)
                listWidget.frame_opacity_slider.sliderMoved.connect(self.setRelativeOpacity)
                self.relative_frame_layout.addWidget(listWidget)

        # remove all remaining frames from onion skin renderer
        # since their visibility is no longer accesible from ui
        for frame in activeFrames:
            core.G_osrInstance.removeRelativeOnion(frame)

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
                listWidget.frame_opacity_slider.setValue(core.G_osrInstance.getAbsoluteOpacity(int(frame)))
                listWidget.addRemoveButton()
                listWidget.frame_visibility_btn.setChecked(core.G_osrInstance.absoluteOnionExists(int(frame)))
                listWidget.frame_remove_btn.clicked.connect(lambda b_frame = frame: self.removeAbsoluteFrame(b_frame))
                listWidget.frame_visibility_btn.toggled.connect(self.toggleAbsoluteFrame)
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
        core.G_osrInstance.addSelectedOnion()
        for obj in pm.selected():
            self.mwdgt_MeshListObjSet.add(obj)
        self.refreshObjectList()
    
    # 
    def removeSelectedObjects(self):
        core.G_osrInstance.removeSelectedOnion()
        for obj in pm.selected():
            if obj in self.mwdgt_MeshListObjSet:
                self.mwdgt_MeshListObjSet.remove(obj)
        self.refreshObjectList()

    #
    def removewdgt_MeshListObj(self, obj):
        try:
            core.G_osrInstance.removewdgt_MeshListObj(obj.fullPath())
        except:
            core.G_osrInstance.removewdgt_MeshListObj(obj.nodeName())
        self.mwdgt_MeshListObjSet.remove(obj)
        self.refreshObjectList()

    #
    def clearOnionObjects(self):
        core.G_osrInstance.clearwdgt_MeshListObjs()
        self.mwdgt_MeshListObjSet.clear()
        self.refreshObjectList()

    # 
    def toggleRelativeFrame(self):
        sender = self.sender()
        frame = sender.parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        sliderValue = sender.parent().findChild(QtWidgets.QSlider, 'frame_opacity_slider').value()
        if sender.isChecked():
            core.G_osrInstance.addRelativeOnion(frame, sliderValue)
        else:
            core.G_osrInstance.removeRelativeOnion(frame)

    #
    def toggleRelativeKeyframeDisplay(self):
        sender = self.sender()
        core.G_osrInstance.setRelativeKeyDisplay(self.sender().isChecked())
        self.saveSettings()

    # 
    def addAbsoluteFrame(self, **kwargs):
        frame = kwargs.setdefault('frame', pm.animation.getCurrentTime())
        if int(frame) not in self.mAbsoluteOnionSet:
            core.G_osrInstance.addAbsoluteOnion(frame, 50)
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
            core.G_osrInstance.addAbsoluteOnion(frame, sliderValue)
        else:
            core.G_osrInstance.removeAbsoluteOnion(frame)
    
    #
    def removeAbsoluteFrame(self, frame):
        core.G_osrInstance.removeAbsoluteOnion(frame)
        self.mAbsoluteOnionSet.remove(frame)
        self.refreshAbsoluteList()

    #
    def clearAbsoluteFrames(self):
        core.G_osrInstance.clearAbsoluteOnions()
        self.mAbsoluteOnionSet.clear()
        self.refreshAbsoluteList()

    # 
    def clearBuffer(self):
        core.G_osrInstance.rotOnions()

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
        core.G_osrInstance.setRelativeOpacity(frame, opacity)

    #
    def setAbsoluteOpacity(self):
        opacity = self.sender().value()
        frame = self.sender().parent().findChild(QtWidgets.QLabel, 'frame_number').text()
        core.G_osrInstance.setAbsoluteOpacity(int(frame), opacity)

    # 
    def setTintStrength(self):
        core.G_osrInstance.setTintStrength(
            self.sender().value()
        )

    # 
    def setAutoClearBuffer(self):
        value = self.sender().isChecked()
        core.G_osrInstance.setAutoClearBuffer(value)

    #
    def changePrefs(self):
        prefUi = OnionPreferences(self)
        if prefUi.exec_():
            values = prefUi.getValues()
            core.G_osrInstance.setMaxBuffer(values['maxBuffer'])
            core.G_osrInstance.setOutlineWidth(values['outlineWidth'])
            core.G_osrInstance.setTintSeed(values['tintSeed'])
            self.mRelativeFrameAmount = values['relativeKeyCount']*2
            self.refreshRelativeFrame()
            self.saveSettings()
            
    #     
    def setRelativeStep(self):
        core.G_osrInstance.setRelativeStep(self.sender().value())
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
        core.G_osrInstance.setGlobalOpacity(self.sender().value())

    #
    def setOnionType(self):
        core.G_osrInstance.setOnionType(self.onionType_cBox.currentIndex())

    #
    def setDrawBehind(self):
        core.G_osrInstance.setDrawBehind(self.drawBehind_chkBx.isChecked())

    #
    def toggleGroupBox(self):
        h = self.sender().maximumHeight()

        if h > 100000:
            self.sender().setMaximumHeight(14)
        else:
            self.sender().setMaximumHeight(200000)

    #
    def setTintType(self):
        tintType = self.tint_type_cBox.currentIndex()
        if tintType == 0:
            self.constant_col_widget.setMaximumHeight(16777215)
            self.constant_col_widget.setEnabled(True)
        else:
            self.constant_col_widget.setMaximumHeight(0)    
            self.constant_col_widget.setEnabled(False)
        core.G_osrInstance.setTintType(tintType)

            
            



    # UTILITY
    # 
    def setOnionColor(self, btn, rgba):
            btn.setStyleSheet('background-color: rgb(%s,%s,%s);'%(rgba[0], rgba[1], rgba[2]))
            core.G_osrInstance.setTint(rgba, btn.objectName())

    #
    def loadSettings(self):
        with open(os.path.join(self.mToolPath,'settings.txt')) as json_file:  
            self.mPrefs = json.load(json_file)
            self.settings_autoClearBuffer.setChecked(self.mPrefs.setdefault('autoClearBuffer',True))
            core.G_osrInstance.setAutoClearBuffer(self.mPrefs.setdefault('autoClearBuffer',True))

            self.relative_keyframes_chkbx.setChecked(self.mPrefs.setdefault('displayKeyframes',True))
            core.G_osrInstance.setRelativeKeyDisplay(self.mPrefs.setdefault('displayKeyframes',True))

            self.setOnionColor(self.relative_futureTint_btn, self.mPrefs.setdefault('rFutureTint',[0,0,125]))
            self.setOnionColor(self.relative_pastTint_btn, self.mPrefs.setdefault('rPastTint',[0,125,0]))
            self.setOnionColor(self.absolute_tint_btn, self.mPrefs.setdefault('aTint', [125,0,0]))
            core.G_osrInstance.setTintSeed(self.mPrefs.setdefault('tintSeed', 0))
            self.tint_type_cBox.setCurrentIndex(self.mPrefs.setdefault('tintType',0))


            self.onionType_cBox.setCurrentIndex(self.mPrefs.setdefault('onionType',1))
            self.drawBehind_chkBx.setChecked(self.mPrefs.setdefault('drawBehind', True))

            self.mRelativeFrameAmount = self.mPrefs.setdefault('relativeFrameAmount',4)
            self.refreshRelativeFrame()
            activeRelativeFrames = self.mPrefs.setdefault('activeRelativeFrames',[])
            for child in self.relative_frame.findChildren(OnionListFrame):
                if int(child.frame_number.text()) in activeRelativeFrames:
                    child.frame_visibility_btn.setChecked(True)

            self.relative_step_spinBox.setValue(self.mPrefs.setdefault('relativeStep', 1))

            core.G_osrInstance.setMaxBuffer(self.mPrefs.setdefault('maxBufferSize', 200))
            core.G_osrInstance.setOutlineWidth(self.mPrefs.setdefault('outlineWidth',3))

    
    # save values into a json file
    def saveSettings(self):
        if DEBUG_ALL: print 'start save'
        data = {}
        data['autoClearBuffer'] = self.settings_autoClearBuffer.isChecked()
        data['displayKeyframes'] = self.relative_keyframes_chkbx.isChecked()
        data['rFutureTint'] = self.extractRGBFromStylesheet(self.relative_futureTint_btn.styleSheet())
        data['rPastTint'] = self.extractRGBFromStylesheet(self.relative_pastTint_btn.styleSheet())
        data['aTint'] = self.extractRGBFromStylesheet(self.absolute_tint_btn.styleSheet())
        data['tintSeed'] = core.G_osrInstance.getTintSeed()
        data['tintType'] = self.tint_type_cBox.currentIndex()
        data['relativeFrameAmount'] = self.mRelativeFrameAmount
        data['relativeStep'] = self.relative_step_spinBox.value()
        data['maxBufferSize'] = core.G_osrInstance.getMaxBuffer()
        data['outlineWidth'] = core.G_osrInstance.getOutlineWidth()
        data['onionType'] = self.onionType_cBox.currentIndex()
        data['drawBehind'] = self.drawBehind_chkBx.isChecked()
        data['activeRelativeFrames'] = self.getActiveRelativeFrameIndices()

        with open(os.path.join(self.mToolPath,'settings.txt'), 'w') as outfile:  
            json.dump(data, outfile)
        if DEBUG_ALL: print 'end save'
        
    # 
    def extractRGBFromStylesheet(self, s):
        return map(int,(s[s.find("(")+1:s.find(")")]).split(','))

    def getActiveRelativeFrameIndices(self):
        activeFrames = []
        # clear the frame of all widgets first
        for child in self.relative_frame.findChildren(OnionListFrame):
            if child.frame_visibility_btn.isChecked():
                activeFrames.append(int(child.frame_number.text()))
        return activeFrames





'''
FRAME WIDGET
the widget for displaying a frame in a list. includes visibility, opacity slider
and on demand a remove button   
'''
class OnionListFrame(QtWidgets.QWidget, wdgt_Frame.Ui_onionSkinFrame_layout):
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
class OnionListObject(QtWidgets.QWidget, wdgt_MeshListObj.Ui_onionSkinObject_layout):
    def __init__(self, parent = getMayaMainWindow()):
        super(OnionListObject, self).__init__(parent)
        self.setupUi(self)



'''
Settings Dialog
in this window the user can set some preferences
'''
class OnionPreferences(QtWidgets.QDialog, wdgt_Preferences.Ui_onionSkinRendererPreferences):
    def __init__(self, parent):
        super(OnionPreferences, self).__init__(parent)
        self.setupUi(self)
        self.relativeKeyCount_spinBox.setValue(parent.mRelativeFrameAmount/2)
        self.maxBuffer_spinBox.setValue(core.G_osrInstance.getMaxBuffer())
        self.outlineWidth_spinBox.setValue(core.G_osrInstance.getOutlineWidth())
        self.tintSeed_spinBox.setValue(core.G_osrInstance.getTintSeed())

    def getValues(self):
        values = {}
        values['maxBuffer'] = self.maxBuffer_spinBox.value()
        values['relativeKeyCount'] = self.relativeKeyCount_spinBox.value()
        values['outlineWidth'] = self.outlineWidth_spinBox.value()
        values['tintSeed'] = self.tintSeed_spinBox.value()
        return values