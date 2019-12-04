import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaAnim as oma
import maya.api.OpenMayaUI as omui
import pymel.core as pm
import os
import inspect
import traceback
import collections
import random

import onionSkinRenderer.core_clearRender as clearRender
import onionSkinRenderer.core_hudRender as hudRender
import onionSkinRenderer.core_presentTarget as presentTarget
import onionSkinRenderer.core_quadRender as quadRender
import onionSkinRenderer.core_sceneRender as sceneRender



"""
This code is a render override for displaying onion skin overlays in the 3D viewport,
which i will refer to as onions in further comments.
It uses render targets to store the rendered onions. Unfortunately as of now it
doesn't interactively update the onions on the fly. Instead it just saves the onion
of the current frame and displays a saved onion from a different frame if available.
"""





"""
Constants & Debug Variables
When something goes wrong, turning these on will
dump info in the script editor
"""
DEBUG_ALL = False
DEBUG_RENDER_OVERIDE = False
DEBUG_SCENE_RENDER = False
DEBUG_QUAD_RENDER = False
PLUGIN_NAME = "Onion Skin Renderer"


"""
Tells maya to use the new api
"""
def maya_useNewAPI():
    pass





# globally available instance of renderer
G_osrInstance = None



'''
Initialize the plugin

This manually registers the osr as a plugin in maya.
Several reasons to do this
- some studios don't allow users to add stuff to their C drive
- convenience, it is a lot easier for users to copy a folder to their scripts directory and be done
- as a plugin I can't get to the G_osrInstance (sth to do with python namespaces i guess)

It feels a bit hacky, but it works anyway

However the downside is that if the tool crashes or for some other reason
doesn't finish the unitializeOverride() function, you need to restart maya for it to work again
'''

def initializeOverride():
    if DEBUG_ALL: print 'initialize Renderer'
    try:
        # register the path to the plugin
        omr.MRenderer.getShaderManager().addShaderPath(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))
        global G_osrInstance
        G_osrInstance = viewRenderOverride("onionSkinRenderer")
        G_osrInstance.createCallbacks()
        omr.MRenderer.registerOverride(G_osrInstance)
    except:
        traceback.print_exc()
        raise Exception("Failed to register plugin %s" %PLUGIN_NAME)
        

# un-init
def uninitializeOverride():
    if DEBUG_ALL: print 'unitiliazide Renderer'
    try:
        global G_osrInstance
        if G_osrInstance is not None:
            omr.MRenderer.deregisterOverride(G_osrInstance)
            G_osrInstance.deleteCallbacks()
            G_osrInstance = None
    except:
        traceback.print_exc()
        raise Exception("Failed to unregister plugin %s" % PLUGIN_NAME)
        





"""
This is the main class for the render overide.
The main thing it does is handling inputs from the controller and rendering the passes.
Think of passes as photoshop layers getting merged and then sent to the screen.
The class also holds all the 
"""
class viewRenderOverride(omr.MRenderOverride):
    # constructor
    def __init__(self, name):
        if DEBUG_ALL or DEBUG_RENDER_OVERIDE:
            print ("Initializing viewRenderOverride")

        #omr.MRenderOverride.__init__(self, name)
        super(viewRenderOverride, self).__init__(name)

        # name in the renderer dropdown menu
        self.UIName = PLUGIN_NAME

        # this counts through the render passes
        # restarts for every frame output to the screen
        self.operation = 0

        # label for the onion
        # current frame, used for setting the onion target key
        self.currentFrame = 0
        # holds all avaialable onions
        # the key to the target is its frame number
        self.onionSkinBuffer = {}
        # save the order in which onions where added
        self.onionSkinBufferQueue = collections.deque()
        # max amount of buffered frames
        self.maxOnionSkinBufferSize = 200
        # manages the display of the onion skin overlay, false means no overlay
        self.enableBlend = False
        # save the relative Onions
        self.relativeOnions = {}
        # only display every nth relative onion
        self.relativeStep = 1
        # save the absolute onions
        self.absoluteOnions = {}
        # buffer onion objects to make adding sets possible
        self.onionObjectBuffer = om.MSelectionList()
        # save all the objects to display in a list
        self.onionObjectList = om.MSelectionList()
        # store the render operations that combine onions in a list
        self.renderOperations = []
        # tint colors for different os types rgb 0-255
        self.relativeFutureTint = [255,0,0]
        self.relativePastTint = [0,255,0]
        self.absoluteTint = [0,0,255]
        # tint strengths, 1 is full tint
        self.tintStrength = 1.0
        self.globalOpacity = 1.0
        self.onionType = 1
        # outline width in pixels
        self.outlineWidth = 3
        self.drawBehind = 1

        # range 0-2.
        # 0 = default, 1 = relative random, 2 = static random
        self.tintType = 0
        # seed value set by user to get different random colors for tints
        self.tintSeed = 0

        # If this is True, we will show onions on the next keyticks
        # e.g. if relativeOnions has 1 and 3 in it, it will draw
        # the next and the 3rd frame with a tick on the timeslider
        self.relativeKeyDisplay = True
        # 
        self.timeCallbackId = 0
        # 
        self.cameraMovedCallbackIds = []
        # 
        self.autoClearBuffer = True

        # Passes
        self.clearPass = clearRender.viewRenderClearRender("clearPass")
        self.clearPass.setOverridesColors(False)
        self.renderOperations.append(self.clearPass)

        self.standardPass = sceneRender.viewRenderSceneRender(
            "standardPass",
            omr.MClearOperation.kClearNone
        )
        self.renderOperations.append(self.standardPass)

        self.onionPass = sceneRender.viewRenderSceneRender(
            "onionPass",
            omr.MClearOperation.kClearAll
        )
        self.onionPass.setSceneFilter(omr.MSceneRender.kRenderShadedItems)
        self.onionPass.setDrawSelectionFilter(True)
        self.renderOperations.append(self.onionPass)

        self.HUDPass = hudRender.viewRenderHUDRender()
        self.renderOperations.append(self.HUDPass)

        self.presentTarget = presentTarget.viewRenderPresentTarget("presentTarget")
        self.renderOperations.append(self.presentTarget)
        
        # TARGETS
        # standard target is what will be displayed. all but onion render to this target
        self.standardTargetDescr = omr.MRenderTargetDescription()
        self.standardTargetDescr.setName("standardTarget")
        self.standardTargetDescr.setRasterFormat(omr.MRenderer.kR8G8B8A8_UNORM)

        # onion target will be blended over standard target
        self.onionTargetDescr = omr.MRenderTargetDescription()
        self.onionTargetDescr.setName("onionTarget")
        self.onionTargetDescr.setRasterFormat(omr.MRenderer.kR8G8B8A8_UNORM)

        # Set the targets that don't change
        self.targetMgr = omr.MRenderer.getRenderTargetManager()
        
        self.standardTarget = self.targetMgr.acquireRenderTarget(self.standardTargetDescr)
        self.clearPass.setRenderTarget(self.standardTarget)
        self.standardPass.setRenderTarget(self.standardTarget)
        self.HUDPass.setRenderTarget(self.standardTarget)
        self.presentTarget.setRenderTarget(self.standardTarget)

    # destructor
    def __del__(self):
        if DEBUG_ALL or DEBUG_RENDER_OVERIDE:
            print ("Deleting viewRenderOverride")
        self.clearPass = None
        self.standardPass = None
        self.HUDPass = None
        self.presentTarget = None
        self.renderOperations = None
        # delete the targets, otherwise the target manager might
        # return None when asked for a target that already exists
        self.rotOnions()
        self.targetMgr.releaseRenderTarget(self.standardTarget)
        self.targetMgr = None
        self.onionObjectList = None
        self.mAnim = None
        


    # -----------------
    # RENDER FUNCTIONS

    # specify that openGl and Directx11 are supported
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices


    # this is basically the render function
    # it is called every refresh of the screen and handles the passes
    def setup(self, destination):
        if DEBUG_ALL or DEBUG_RENDER_OVERIDE:
            print ("Starting setup")
        # set the size of the target, so when the viewport scales,
        # the targets remain a 1:1 pixel size
        targetSize = omr.MRenderer.outputTargetSize()
        self.standardTargetDescr.setWidth(targetSize[0])
        self.standardTargetDescr.setHeight(targetSize[1])
        self.onionTargetDescr.setWidth(targetSize[0])
        self.onionTargetDescr.setHeight(targetSize[1])

        # update the standard target to the just set size
        self.standardTarget.updateDescription(self.standardTargetDescr)
        # update the onion target to a new name, because targetMgr will return None
        # if the name already exists
        self.currentFrame = oma.MAnimControl.currentTime().value
        onionTargetName = "onionTarget%s" % self.currentFrame
        self.onionTargetDescr.setName(onionTargetName)
        
        # if the onion is not buffered do so, otherwise update the buffered
        if self.currentFrame not in self.onionSkinBuffer:
            self.onionSkinBuffer[self.currentFrame] = self.targetMgr.acquireRenderTarget(self.onionTargetDescr)
            self.onionSkinBufferQueue.append(self.currentFrame)
            if len(self.onionSkinBufferQueue) > self.maxOnionSkinBufferSize: self.rotOldestOnion()
        else:
            self.onionSkinBuffer.get(self.currentFrame).updateDescription(self.onionTargetDescr)
        # then set the render target to the appropriate onion
        self.onionPass.setRenderTarget(self.onionSkinBuffer.get(self.currentFrame))
        # set the filter list to the onion renderer
        self.onionPass.setObjectFilterList(self.onionObjectList)

        # setting targets to relative blend passes
        for blend in self.relativeOnions:
            blendPass = self.relativeOnions[blend]
            targetFrame = 1
            if self.relativeKeyDisplay:
                targetFrame = blendPass.mFrame
            else:
                targetFrame = blendPass.mFrame * self.relativeStep + self.currentFrame
            

            if targetFrame in self.onionSkinBuffer:
                if not self.relativeKeyDisplay:
                    blendPass.setActive(True)
                blendPass.setInputTargets(self.standardTarget, self.onionSkinBuffer[targetFrame])
                blendPass.setStencilTarget(self.onionSkinBuffer[self.currentFrame])

                # Constant Color
                if self.tintType == 0:
                    # future tint
                    if targetFrame > self.currentFrame:
                        blendPass.setTint((
                            self.relativeFutureTint[0]/255.0 / self.lerp(1.0, self.relativeFutureTint[0]/255.0, self.tintStrength),
                            self.relativeFutureTint[1]/255.0 / self.lerp(1.0, self.relativeFutureTint[1]/255.0, self.tintStrength), 
                            self.relativeFutureTint[2]/255.0 / self.lerp(1.0, self.relativeFutureTint[2]/255.0, self.tintStrength), 
                            1.0))
                    # past tint
                    else:
                        blendPass.setTint((
                            self.relativePastTint[0]/255.0 / self.lerp(1.0, self.relativePastTint[0]/255.0, self.tintStrength),
                            self.relativePastTint[1]/255.0 / self.lerp(1.0, self.relativePastTint[1]/255.0, self.tintStrength), 
                            self.relativePastTint[2]/255.0 / self.lerp(1.0, self.relativePastTint[2]/255.0, self.tintStrength),  
                            1.0))
                # Relative Random
                elif self.tintType == 1:
                    random.seed(blendPass.mFrame + self.tintSeed + 1)
                    blendPass.setTint((
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        1.0
                    ))
                # Static Random
                else:
                    # using the frame as a random seed,
                    # so each frame always has a static color
                    random.seed(targetFrame + self.tintSeed)
                    blendPass.setTint((
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        1.0
                    ))
            else:
                blendPass.setActive(False)

        # setting targets to absolute blendPasses
        for blend in self.absoluteOnions:
            blendPass = self.absoluteOnions[blend]
            
            if blendPass.mFrame in self.onionSkinBuffer:
                blendPass.setActive(True)
                blendPass.setInputTargets(self.standardTarget, self.onionSkinBuffer[blendPass.mFrame])
                blendPass.setStencilTarget(self.onionSkinBuffer[self.currentFrame])
                if self.tintType == 0:
                    blendPass.setTint((
                        self.absoluteTint[0]/255.0 / self.lerp(1.0, self.absoluteTint[0]/255.0, self.tintStrength),
                        self.absoluteTint[1]/255.0 / self.lerp(1.0, self.absoluteTint[1]/255.0, self.tintStrength),
                        self.absoluteTint[2]/255.0 / self.lerp(1.0, self.absoluteTint[2]/255.0, self.tintStrength)
                    ))
                else:
                    random.seed(blendPass.mFrame + self.tintSeed)
                    blendPass.setTint((
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        random.randrange(0,100)/100.0,
                        1.0
                    ))

            else:
                blendPass.setActive(False)

            

    # called by maya to start iterating through passes
    def startOperationIterator(self):
        self.operation = 0
        return True

    # called by maya to define which pass to calculate
    # the order specified here defines the draw order
    def renderOperation(self):
        return self.renderOperations[self.operation]

    # advance to the next pass or return false if
    # all are calculated
    def nextRenderOperation(self):
        self.operation = self.operation + 1
        return self.operation < len(self.renderOperations)






    # -----------------
    # UTILITY FUNCTIONS

    # reducing code duplicates by merging both add onion functions
    def addOnion(self, frame, opacity, targetDict):
        if frame not in targetDict:
            targetDict[frame] = viewRenderQuadRender(
                'blendPass%s' % frame,
                omr.MClearOperation.kClearNone,
                int(frame)
            )
            targetDict[frame].setOpacity(opacity/100.0)
            targetDict[frame].setShader(viewRenderQuadRender.kSceneBlend)
            targetDict[frame].setRenderTarget(self.standardTarget)

            # insert operation after onion pass
            self.renderOperations.insert(
                self.renderOperations.index(self.onionPass) + 1,
                targetDict[frame]
            )


        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # called by absolute and relative remove
    def removeOnion(self, frame, targetDict):
        if frame in targetDict:
            renderPass = targetDict.pop(frame, None)
            self.renderOperations.remove(renderPass)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # called by maya. Sets the name in the "Renderers" dropdown
    def uiName(self):
        return self.UIName
    
    #
    def rotOnions(self, refresh = True):
        if self.targetMgr is not None:
            for target in self.onionSkinBuffer:
                self.targetMgr.releaseRenderTarget(self.onionSkinBuffer.get(target))
        self.onionSkinBuffer.clear()
        self.onionSkinBufferQueue.clear()
        if refresh: omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # 
    def rotOldestOnion(self):
        frame = self.onionSkinBufferQueue.popleft()
        if self.targetMgr is not None:
            self.targetMgr.releaseRenderTarget(self.onionSkinBuffer[frame])
        self.onionSkinBuffer.pop(frame)

    #
    def lerp(self, start, end, factor):
        if factor < 1 and factor > 0:
            return (factor * start) + ((1-factor) * end)
        else:
            return start

    # change the frame display to the right keys relative to timeslider position
    def setRelativeFrames(self, value):
        if not self.relativeKeyDisplay:
            return
        
        nextKeys = []
        pastKeys = []

        nextKey = pm.findKeyframe(ts=True, w="next")
        pastKey = pm.findKeyframe(ts=True, w="previous")

        # add next keys to list
        bufferKey = pm.getCurrentTime()
        for i in range(4):
            if nextKey <= bufferKey:
                break
            nextKeys.append(nextKey)
            bufferKey = nextKey
            nextKey = pm.findKeyframe(t=bufferKey, ts=True, w="next")

        # add prev keys to list
        bufferKey = pm.getCurrentTime()
        for i in range(4):
            if pastKey >= bufferKey:
                break
            pastKeys.append(pastKey)
            bufferKey = pastKey
            pastKey = pm.findKeyframe(t=bufferKey, ts=True, w="previous")


        pastKeys = list(reversed(pastKeys))

        for frameIndex in self.relativeOnions:
            blendPass = self.relativeOnions[frameIndex]
            if frameIndex < 0:
                # past
                if pastKeys and len(pastKeys) >= frameIndex*-1:
                    blendPass.setActive(True)
                    blendPass.setFrame(pastKeys[frameIndex])
                else:
                    blendPass.setActive(False)
            else: 
                # future
                if nextKeys and len(nextKeys) >= frameIndex:
                    blendPass.setActive(True)
                    blendPass.setFrame(nextKeys[frameIndex-1])
                else:
                    blendPass.setActive(False)
    
    # 
    def flattenSelectionList(self, selList):
        flatList = om.MSelectionList()
        selIter = om.MItSelectionList(selList)
        while not selIter.isDone():
            obj = selIter.getDependNode()
            # if its a DAG node
            if selIter.itemType() == 0:
                if selIter.hasComponents():
                    flatList.add(selIter.getComponent())
                # just add it to the list if it's a dag object
                elif obj.hasFn(om.MFn.kDagNode):
                    flatList.add(selIter.getDagPath())
            # if its a set recursive call with set contents
            elif obj.hasFn(om.MFn.kSet):
                flatList.merge(self.flattenSelectionList(om.MFnSet(obj).getMembers(False)))

            selIter.next()
        return flatList

    # attached to all cameras found on plugin launch, removes onions when the camera moves
    # but only on user input. animated cameras are not affected
    def cameraMovedCB(self, msg, plug1, plug2, payload):
        if (msg == 2056 
            and self.autoClearBuffer
            and (self.isPlugInteresting(plug1, 'translate') 
            or self.isPlugInteresting(plug1, 'rotate'))):
            self.rotOnions(False)

    # checks if the plug matches the given string
    def isPlugInteresting(self, plug, targetPlug):
        mfn_dep = om.MFnDependencyNode(plug.node())
        return plug == mfn_dep.findPlug(targetPlug, True)

    #
    def refresh(self):
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

        





    # ----------------
    # INTERFACE FUNCTIONS

    # add a frame to display relative to current time slider position
    def addRelativeOnion(self, frame, opacity):
        self.addOnion(int(frame), opacity, self.relativeOnions)

    #
    def removeRelativeOnion(self, frame):
        self.removeOnion(int(frame), self.relativeOnions)

    def setRelativeKeyDisplay(self, value):
        self.relativeKeyDisplay = value
        if value:
            self.setRelativeFrames(1)
        else:
            for frameIndex in self.relativeOnions:
                blendPass = self.relativeOnions[frameIndex]
                blendPass.setFrame(frameIndex)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)
    
    # add a frame that is always displayed on the current position
    def addAbsoluteOnion(self, frame, opacity):
        self.addOnion(int(frame), opacity, self.absoluteOnions)
    
    #
    def removeAbsoluteOnion(self, frame):
        self.removeOnion(int(frame), self.absoluteOnions)

    #
    def clearAbsoluteOnions(self):
        for onion in self.absoluteOnions:
            self.renderOperations.remove(self.absoluteOnions[onion])
        self.absoluteOnions.clear()
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def absoluteOnionExists(self, frame):
        return frame in self.absoluteOnions

    #
    def getAbsoluteOpacity(self, frame):
        if frame in self.absoluteOnions:
            return self.absoluteOnions[frame].mOpacity * 100
        
        return 50

    # 
    def setTint(self, rgba, target):
        if target == 'relative_futureTint_btn':
            self.relativeFutureTint = rgba
        elif target == 'relative_pastTint_btn':
            self.relativePastTint = rgba
        elif target == 'absolute_tint_btn':
            self.absoluteTint = rgba

        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)
    
    #
    def setTintStrength(self, strength):
        self.tintStrength = strength / 100.0
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)


    #
    def setRelativeOpacity(self, frame, opacity):
        if int(frame) in self.relativeOnions:
            self.relativeOnions[int(frame)].setOpacity(opacity/100.0)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    def setGlobalOpacity(self, opacity):
        self.globalOpacity = opacity/100.0
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def setAbsoluteOpacity(self, frame, opacity):
        if frame in self.absoluteOnions:
            self.absoluteOnions[frame].setOpacity(opacity/100.0)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # adding objects to the selectionList
    # works recursively if a set is found
    def addSelectedOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.onionObjectBuffer.merge(selList)
        self.onionObjectList = self.flattenSelectionList(self.onionObjectBuffer)
        self.rotOnions()

    #
    def removeSelectedOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.onionObjectBuffer.merge(selList, om.MSelectionList.kRemoveFromList)
        self.onionObjectList = self.flattenSelectionList(self.onionObjectBuffer)
        self.rotOnions()

    #
    def removeOnionObject(self, dagPath):
        tmpList = om.MSelectionList()
        tmpList.add(dagPath)
        self.onionObjectBuffer.merge(tmpList, om.MSelectionList.kRemoveFromList)
        self.onionObjectList = self.flattenSelectionList(self.onionObjectBuffer)
        self.rotOnions()

    #
    def clearOnionObjects(self):
        self.onionObjectList = om.MSelectionList()
        self.onionObjectBuffer = om.MSelectionList()
        self.rotOnions()

    # adding callbacks to the scene
    def createCallbacks(self):
        # frame changed callback
        # needed for changing the relative keyframe display
        self.timeCallbackId = om.MEventMessage.addEventCallback('timeChanged', self.setRelativeFrames)
        # iterate over all cameras add the callback
        dgIter = om.MItDependencyNodes(om.MFn.kCamera)
        while not dgIter.isDone():
            shape = om.MFnDagNode(dgIter.thisNode())
            transform = shape.parent(0)
            if transform is not None:
                self.cameraMovedCallbackIds.append(
                    om.MNodeMessage.addAttributeChangedCallback(transform, self.cameraMovedCB))
            dgIter.next()

    # removing them when the ui is closed
    def deleteCallbacks(self):
        om.MEventMessage.removeCallback(self.timeCallbackId)
        for id in self.cameraMovedCallbackIds:
            om.MMessage.removeCallback(id)
        self.cameraMovedCallbackIds = []

    # define if the buffer should be cleared when the camera moves
    def setAutoClearBuffer(self, value):
        self.autoClearBuffer = value

    # 
    def setMaxBuffer(self, value):
        self.maxOnionSkinBufferSize = value
        while len(self.onionSkinBufferQueue) > self.maxOnionSkinBufferSize:
            self.rotOldestOnion()
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)
        
    # 
    def getMaxBuffer(self):
        return self.maxOnionSkinBufferSize

    # 
    def setRelativeStep(self, value):
        self.relativeStep = value
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # 
    def setOnionType(self, onionType):
        self.onionType = onionType
        self.refresh()
    
    # 
    def setOutlineWidth(self, width):
        self.outlineWidth = width
        self.refresh()

    # 
    def getOutlineWidth(self):
        return self.outlineWidth
        
    #
    def setDrawBehind(self, value):
        self.drawBehind = int(value)
        self.refresh()

    #
    def getDrawBehind(self):
        return self.drawBehind

    #
    def setTintType(self, tintType):
        self.tintType = tintType
        self.refresh()

    #
    def setTintSeed(self, seed):
        self.tintSeed = seed
        self.refresh()

    #
    def getTintSeed(self):
        return self.tintSeed

