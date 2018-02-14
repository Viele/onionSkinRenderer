import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaAnim as oma
import maya.api.OpenMayaUI as omui
import pymel.core as pm
import os
import inspect
import traceback

"""
This code is a render override for displaying onion skin overlays in the 3D viewport,
which i will refer to as onions in further comments.
It uses render targets to store the rendered onions. Unfortunately as of now it
doesn't interactively update the onions on the fly. Instead it just saves the onion
of the current frame and displays a saved onion from a different frame if available.

Since I am not really a programmer and I think it helps understanding the code, further comments will
follow a story:
You are a little kid preparing a vegetable plate for your Mom. Your Mom, which I will refer to as M,
sometimes wants you to show her certain onions from these veggies.
You have to manage a sequence of these onions,
and if requested display a certain number of them
"""

"""
TODO
-some interaction with maya causes the onions to become invalid(not correct),
    e.g. rotating camera, adding/removing objs from onion list
    in this case the onions shouldn't be displayed unless they are updated
-show next keyframes
"""


"""
Constants
When M is so unhappy with your work that it refuses it,
start here to see whats wrong
"""
kDebugAll = False
kDebugRenderOverride = False
kDebugSceneRender = False
kDebugQuadRender = False
kPluginName = "Onion Skin Renderer"


"""
Tell M that you are using the new tools
"""
def maya_useNewAPI():
    pass


"""
Initialize the plugin
This tells M your name and that you are available for work
"""

# globally available instance of renderer
viewRenderOverrideInstance = None

# init
def initializeOverride():
    try:
        # register the path to the plugin
        omr.MRenderer.getShaderManager().addShaderPath(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))
        global viewRenderOverrideInstance
        viewRenderOverrideInstance = viewRenderOverride("onionSkinRenderer")
        viewRenderOverrideInstance.createCallback()
        omr.MRenderer.registerOverride(viewRenderOverrideInstance)
    except:
        raise Exception("Failed to register plugin %s" %kPluginName)
        

# un-init
def uninitializeOverride():
    try:
        global viewRenderOverrideInstance
        if viewRenderOverrideInstance is not None:
            omr.MRenderer.deregisterOverride(viewRenderOverrideInstance)
            viewRenderOverrideInstance.deleteCallback()
            viewRenderOverrideInstance = None
    except:
        raise Exception("Failed to unregister plugin %s" % kPluginName)
        


"""
If M requires your help, you start your work here.
This is a custom vegetable preparation workstation, but fortunately you didn't need to create it from scratch.
It basically extends the standard workstation, but modifies it for onion management.
In the workstation there is a sequence of onions, which are labeled with numbers that correspond to a
certain place in time
"""
class viewRenderOverride(omr.MRenderOverride):
    # constructor
    def __init__(self, name):
        if kDebugAll or kDebugRenderOverride:
            print ("Initializing viewRenderOverride")

        #omr.MRenderOverride.__init__(self, name)
        super(viewRenderOverride, self).__init__(name)
        # name in the renderer dropdown menu
        self.mUIName = kPluginName
        # everytime you are preparing a plate,
        # you have to count which step you are on
        # this is reset when you start a new plate
        self.mOperation = 0
        # label for the onion
        # current frame, used for setting the onion target key
        self.mCurrentFrame = 0
        # holds all avaialable onions
        # the key to the target is its frame number
        self.mOnionBuffer = {}
        # sometimes M doesn't want to see onions,
        # thats when this should be False
        self.mEnableBlend = False
        # save the relative Onions
        self.mRelativeOnions = {}
        # save the absolute onions
        self.mAbsoluteOnions = {}
        # save all the objects to display in a list
        self.mOnionObjectList = om.MSelectionList()
        # store the render operations that combine onions in a list
        self.mRenderOperations = []
        # the tints for onions
        self.mRelativeFutureTint = [255,0,0]
        self.mRelativePastTint = [0,255,0]
        self.mAbsoluteTint = [0,0,255]
        # tint strengths, 1 is full tint
        self.mRelativeTintStrength = 1.0
        self.mAbsoluteTintStrength = 1.0

        # If this is True, we will show onions on the next keyticks
        # e.g. if mRelativeOnions has 1 and 3 in it, it will draw
        # the next and the 3rd frame with a tick on the timeslider
        self.mRelativeKeyDisplay = True
        self.mCallbackId = 0

        # Passes
        self.mClearPass = viewRenderClearRender("clearPass")
        self.mClearPass.setOverridesColors(False)
        self.mRenderOperations.append(self.mClearPass)

        self.mStandardPass = viewRenderSceneRender(
            "standardPass",
            omr.MClearOperation.kClearNone
        )
        self.mRenderOperations.append(self.mStandardPass)

        self.mOnionPass = viewRenderSceneRender(
            "onionPass",
            omr.MClearOperation.kClearAll
        )
        self.mOnionPass.setSceneFilter(omr.MSceneRender.kRenderShadedItems)
        self.mOnionPass.setDrawSelectionFilter(True)
        self.mRenderOperations.append(self.mOnionPass)

        self.mHUDPass = viewRenderHUDRender()
        self.mRenderOperations.append(self.mHUDPass)

        self.mPresentTarget = viewRenderPresentTarget("presentTarget")
        self.mRenderOperations.append(self.mPresentTarget)
        
        # TARGETS
        # standard target is what will be displayed. all but onion render to this target
        self.mStandardTargetDescr = omr.MRenderTargetDescription()
        self.mStandardTargetDescr.setName("standardTarget")
        self.mStandardTargetDescr.setRasterFormat(omr.MRenderer.kR8G8B8A8_UNORM)

        # onion target will be blended over standard target
        self.mOnionTargetDescr = omr.MRenderTargetDescription()
        self.mOnionTargetDescr.setName("onionTarget")
        self.mOnionTargetDescr.setRasterFormat(omr.MRenderer.kR8G8B8A8_UNORM)

        # Set the targets that don't change
        self.mTargetMgr = omr.MRenderer.getRenderTargetManager()
        
        self.mStandardTarget = self.mTargetMgr.acquireRenderTarget(self.mStandardTargetDescr)
        self.mClearPass.setRenderTarget(self.mStandardTarget)
        self.mStandardPass.setRenderTarget(self.mStandardTarget)
        self.mHUDPass.setRenderTarget(self.mStandardTarget)
        self.mPresentTarget.setRenderTarget(self.mStandardTarget)

    # destructor
    def __del__(self):
        if kDebugAll or kDebugRenderOverride:
            print ("Deleting viewRenderOverride")
        self.mClearPass = None
        self.mStandardPass = None
        self.mHUDPass = None
        self.mPresentTarget = None
        self.mRenderOperations = None
        # delete the targets, otherwise the target manager might
        # return None when asked for a target that already exists
        self.rotOnions()
        self.mTargetMgr.releaseRenderTarget(self.mStandardTarget)
        self.mTargetMgr = None
        self.mOnionObjectList = None
        self.mAnim = None
        


    # -----------------
    # RENDER FUNCTIONS

    # specify that openGl and Directx11 are supported
    def supportedDrawAPIs(self):
        return omr.MRenderer.kOpenGLCoreProfile

    # before sorting veggies on your plate, prepare your workspace
    def setup(self, destination):
        if kDebugAll or kDebugRenderOverride:
            print ("Starting setup")
        # set the size of the target, so when the viewport scales,
        # the targets remain a 1:1 pixel size
        targetSize = omr.MRenderer.outputTargetSize()
        self.mStandardTargetDescr.setWidth(targetSize[0])
        self.mStandardTargetDescr.setHeight(targetSize[1])
        self.mOnionTargetDescr.setWidth(targetSize[0])
        self.mOnionTargetDescr.setHeight(targetSize[1])

        # update the standard target to the just set size
        self.mStandardTarget.updateDescription(self.mStandardTargetDescr)
        # update the onion target to a new name, because targetMgr will return None
        # if the name already exists
        self.mCurrentFrame = oma.MAnimControl.currentTime().value
        onionTargetName = "onionTarget%s" % self.mCurrentFrame
        self.mOnionTargetDescr.setName(onionTargetName)
        
        # if the onion is not buffered do so, otherwise update the buffered
        if self.mCurrentFrame not in self.mOnionBuffer:
            self.mOnionBuffer[self.mCurrentFrame] = self.mTargetMgr.acquireRenderTarget(self.mOnionTargetDescr)
        else:
            self.mOnionBuffer.get(self.mCurrentFrame).updateDescription(self.mOnionTargetDescr)
        # then set the render target to the appropriate onion
        self.mOnionPass.setRenderTarget(self.mOnionBuffer.get(self.mCurrentFrame))
        # set the filter list to the onion renderer
        self.mOnionPass.setObjectFilterList(self.mOnionObjectList)

        # setting targets to relative blend passes
        for blend in self.mRelativeOnions:
            blendPass = self.mRelativeOnions[blend]
            targetFrame = 1
            if self.mRelativeKeyDisplay:
                targetFrame = blendPass.mFrame
            else:
                targetFrame = blendPass.mFrame + self.mCurrentFrame

            if targetFrame in self.mOnionBuffer:
                if not self.mRelativeKeyDisplay:
                    blendPass.setActive(True)
                blendPass.setInputTargets(self.mStandardTarget, self.mOnionBuffer[targetFrame])
                # future tint
                if targetFrame > self.mCurrentFrame:
                    blendPass.setTint((
                        (self.mRelativeFutureTint[0]/255.0) / self.lerp(1.0, self.mRelativeFutureTint[0]/255.0, self.mRelativeTintStrength),
                        self.mRelativeFutureTint[1]/255.0 / self.lerp(1.0, self.mRelativeFutureTint[1]/255.0, self.mRelativeTintStrength), 
                        self.mRelativeFutureTint[2]/255.0 / self.lerp(1.0, self.mRelativeFutureTint[2]/255.0, self.mRelativeTintStrength), 
                        1.0))
                # past tint
                else:
                    blendPass.setTint((
                        self.mRelativePastTint[0]/255.0 / self.lerp(1.0, self.mRelativePastTint[0]/255.0, self.mRelativeTintStrength),
                        self.mRelativePastTint[1]/255.0 / self.lerp(1.0, self.mRelativePastTint[1]/255.0, self.mRelativeTintStrength), 
                        self.mRelativePastTint[2]/255.0 / self.lerp(1.0, self.mRelativePastTint[2]/255.0, self.mRelativeTintStrength),  
                        1.0))
            else:
                #pass
                blendPass.setActive(False)

        # setting targets to absolute blendPasses
        for blend in self.mAbsoluteOnions:
            blendPass = self.mAbsoluteOnions[blend]
            
            if blendPass.mFrame in self.mOnionBuffer:
                blendPass.setActive(True)
                blendPass.setInputTargets(self.mStandardTarget, self.mOnionBuffer[blendPass.mFrame])
                blendPass.setTint((
                    self.mAbsoluteTint[0]/255.0 / self.lerp(1.0, self.mAbsoluteTint[0]/255.0, self.mAbsoluteTintStrength),
                    self.mAbsoluteTint[1]/255.0 / self.lerp(1.0, self.mAbsoluteTint[1]/255.0, self.mAbsoluteTintStrength),
                    self.mAbsoluteTint[2]/255.0 / self.lerp(1.0, self.mAbsoluteTint[2]/255.0, self.mAbsoluteTintStrength)
                ))
            else:
                blendPass.setActive(False)

            

    # called by maya to start iterating through passes
    def startOperationIterator(self):
        self.mOperation = 0
        return True

    # called by maya to define which pass to calculate
    # the order specified here defines the draw order
    def renderOperation(self):
        return self.mRenderOperations[self.mOperation]

    # advance to the next pass or return false if
    # all are calculated
    def nextRenderOperation(self):
        self.mOperation = self.mOperation + 1
        return self.mOperation < len(self.mRenderOperations)


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
            targetDict[frame].setRenderTarget(self.mStandardTarget)

            # insert operation after onion pass
            self.mRenderOperations.insert(
                self.mRenderOperations.index(self.mOnionPass) + 1,
                targetDict[frame]
            )


        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # called by absolute and relative remove
    def removeOnion(self, frame, targetDict):
        if frame in targetDict:
            renderPass = targetDict.pop(frame, None)
            self.mRenderOperations.remove(renderPass)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    # called by maya. Sets the name in the "Renderers" dropdown
    def uiName(self):
        return self.mUIName
    
    #
    def rotOnions(self):
        if self.mTargetMgr is not None:
            for target in self.mOnionBuffer:
                self.mTargetMgr.releaseRenderTarget(self.mOnionBuffer.get(target))
        self.mOnionBuffer.clear()
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def lerp(self, start, end, factor):
        if factor < 1 and factor > 0:
            return (factor * start) + ((1-factor) * end)
        else:
            return start

    # change the frame display to the right keys
    def setRelativeFrames(self, value):
        if not self.mRelativeKeyDisplay:
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

        for frameIndex in self.mRelativeOnions:
            blendPass = self.mRelativeOnions[frameIndex]
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





    # ----------------
    # INTERFACE FUNCTIONS

    # add a frame to display relative to current time slider position
    def addRelativeOnion(self, frame, opacity):
        self.addOnion(int(frame), opacity, self.mRelativeOnions)

    #
    def removeRelativeOnion(self, frame):
        self.removeOnion(int(frame), self.mRelativeOnions)

    def setRelativeKeyDisplay(self, value):
        self.mRelativeKeyDisplay = value
        if value:
            self.setRelativeFrames(1)
        else:
            for frameIndex in self.mRelativeOnions:
                blendPass = self.mRelativeOnions[frameIndex]
                blendPass.setFrame(frameIndex)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)
    
    # add a frame that is always displayed on the current position
    def addAbsoluteOnion(self, frame, opacity):
        self.addOnion(int(frame), opacity, self.mAbsoluteOnions)
    
    #
    def removeAbsoluteOnion(self, frame):
        self.removeOnion(int(frame), self.mAbsoluteOnions)

    #
    def clearAbsoluteOnions(self):
        for onion in self.mAbsoluteOnions:
            self.mRenderOperations.remove(self.mAbsoluteOnions[onion])
        self.mAbsoluteOnions.clear()
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def absoluteOnionExists(self, frame):
        return frame in self.mAbsoluteOnions

    #
    def getAbsoluteOpacity(self, frame):
        if frame in self.mAbsoluteOnions:
            return self.mAbsoluteOnions[frame].mOpacity * 100
        
        return 50

    # 
    def setTint(self, rgba, target):
        if target == 'relative_futureTint_btn':
            self.mRelativeFutureTint = rgba
        elif target == 'relative_pastTint_btn':
            self.mRelativePastTint = rgba
        elif target == 'absolute_tint_btn':
            self.mAbsoluteTint = rgba

        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)
    
    #
    def setRelativeTintStrength(self, strength):
        self.mRelativeTintStrength = strength / 100.0
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def setAbsoluteTintStrength(self, strength):
        self.mAbsoluteTintStrength = strength / 100.0
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def setRelativeOpacity(self, frame, opacity):
        if int(frame) in self.mRelativeOnions:
            self.mRelativeOnions[int(frame)].setOpacity(opacity/100.0)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def setAbsoluteOpacity(self, frame, opacity):
        if frame in self.mAbsoluteOnions:
            self.mAbsoluteOnions[frame].setOpacity(opacity/100.0)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def addSelectedOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.mOnionObjectList.merge(selList)
        self.rotOnions()

    #
    def removeSelectedOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.mOnionObjectList.merge(selList, om.MSelectionList.kRemoveFromList)
        self.rotOnions()

    #
    def removeOnionObject(self, dagPath):
        tmpList = om.MSelectionList()
        tmpList.add(dagPath)
        self.mOnionObjectList.merge(tmpList, om.MSelectionList.kRemoveFromList)
        self.rotOnions()

    #
    def clearOnionObjects(self):
        self.mOnionObjectList = om.MSelectionList()
        self.rotOnions()

    #
    def createCallback(self):
        # frame changed callback
        # needed for changing the relative keyframe display
        self.mCallbackId = om.MEventMessage.addEventCallback('timeChanged', self.setRelativeFrames)

    #
    def deleteCallback(self):
        om.MEventMessage.removeCallback(self.mCallbackId)


    


"""
This is the main tool of your workstation.
In your workstation, you have TWO versions of that tool.
The first version displays the ENTIRE vegetable heap.
The second version ONLY displays the onions in that heap.
It's like a super cool xRay to show your M how neatly
you arranged those onions
"""
class viewRenderSceneRender(omr.MSceneRender):
    def __init__(self, name, clearMask):
        if kDebugAll or kDebugSceneRender:
            print ("Initializing viewRenderSceneRender")
        #omr.MSceneRender.__init__(self, name)
        super(viewRenderSceneRender,self).__init__(name, 'Onion')
        self.mClearMask = clearMask
        self.mPanelName = ""
        self.mDrawSelectionFilter = False
        self.mOnionObjectList = om.MSelectionList()
        self.mTarget = None
        self.mSceneFilter = omr.MSceneRender.kNoSceneFilterOverride

    def __del__(self):
        if kDebugAll or kDebugSceneRender:
            print ("Deleting viewRenderSceneRender")
        self.mSelectionList = None
        self.mTarget = None

    # draw only selected objects if mDrawSelectionFilter is True
    def objectSetOverride(self):
        if self.mDrawSelectionFilter:
            return self.mOnionObjectList
        return None

    # called from viewRenderOverride which manages the list
    def setObjectFilterList(self, selectionList):
        self.mOnionObjectList = selectionList

    # sets the clear mask
    def clearOperation(self):
        self.mClearOperation.setClearColor((0.0, 0.0, 0.0, 0.0))
        self.mClearOperation.setMask(self.mClearMask)
        return self.mClearOperation

    # allows setting the draw selection filter which will only
    # draw selected objects
    def setDrawSelectionFilter(self, flag):
        self.mDrawSelectionFilter = flag

    def setRenderTarget(self, target):
        self.mTarget = target

    def targetOverrideList(self):
        if self.mTarget is not None:
            if kDebugAll or kDebugSceneRender:
                print ("Returning target %s" % self.mTarget)
            return [self.mTarget]
        return None
    
    def setSceneFilter(self, filter):
        self.mSceneFilter = filter

    def renderFilterOverride(self):
        return self.mSceneFilter

"""
M doesn't want to see only onions, but also the surrounding veggies.
With this tool, you can combine displays so you can show them at
the same time
"""
class viewRenderQuadRender(omr.MQuadRender):
    kEffectNone = 0
    kSceneBlend = 1

    def __init__(self, name, clearMask, frame):
        if kDebugAll:
            print ("Initializing viewRenderQuadRender")
        omr.MQuadRender.__init__(self, name)

        self.mShaderInstance = None

        self.mClearMask = clearMask

        self.mTarget = None
        self.mInputTarget = [None, None]

        self.mShader = self.kEffectNone

        self.mFrame = frame

        self.mActive = True

        self.mTint = [1,1,1,1]

        self.mOpacity = 0.5

        

    def __del__(self):
        if kDebugAll:
            print ("Deleting viewRenderQuadRender")
        if self.mShaderInstance is not None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if shaderMgr is not None:
                shaderMgr.releaseShader(self.mShaderInstance)
            self.mShaderInstance = None
        self.mTarget = None
        self.mInputTarget = None

    def shader(self):
        if kDebugAll or kDebugQuadRender:
            print ("Setting up shader")
        if not self.mActive:
            return None

        if self.mShaderInstance is None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if self.mShader == self.kSceneBlend:
                self.mShaderInstance = shaderMgr.getEffectsFileShader("onionSkinShader", "Main", useEffectCache = True)
        if self.mShaderInstance is not None:
            if kDebugAll or kDebugQuadRender:
                print ("Blend target 1: %s" % self.mInputTarget[0])
                print ("Blend target 2: %s" % self.mInputTarget[1])
            self.mShaderInstance.setParameter("gSourceTex", self.mInputTarget[0])
            self.mShaderInstance.setParameter("gSourceTex2", self.mInputTarget[1])
            self.mShaderInstance.setParameter("gBlendSrc", self.mOpacity)
            self.mShaderInstance.setParameter("gTint", self.mTint)

        return self.mShaderInstance

    def targetOverrideList(self):
        if self.mTarget is not None:
            return [self.mTarget]
        return None

    def setRenderTarget(self, target):
        self.mTarget = target

    def clearOperation(self):
        self.mClearOperation.setMask(self.mClearMask)
        return self.mClearOperation

    def setShader(self, shader):
        self.mShader = shader

    def setInputTargets(self, target1, target2):
        self.mInputTarget[0] = target1
        self.mInputTarget[1] = target2
    
    def setActive(self, flag):
        self.mActive = flag

    def setTint(self, tint):
        self.mTint = tint
    
    def setOpacity(self, opacity):
        self.mOpacity = opacity

    def setFrame(self, frame):
        self.mFrame = frame



"""
When M requests a new display, you first have to clear your plate.
This happens with this tool. The plate will have a the color that M
defines.
"""
class viewRenderClearRender(omr.MClearOperation):
    def __init__(self, name):
        omr.MClearOperation.__init__(self, name)

        self.mTarget = None

    def __del__(self):
        self.mTarget = None

    def targetOverrideList(self):
        if self.mTarget is not None:
            return [self.mTarget]
        return None

    def setRenderTarget(self, target):
        self.mTarget = target


"""
Adding the last fancy doodads to your plate
"""
class viewRenderHUDRender(omr.MHUDRender):
    def __init__(self):
        omr.MHUDRender.__init__(self)

        self.mTarget = None

    def __del__(self):
        self.mTarget = None

    def targetOverrideList(self):
        if self.mTarget is not None:
            return [self.mTarget]
        return None

    def setRenderTarget(self, target):
        self.mTarget = target

"""
Turn around and hope M is happy with the result
"""
class viewRenderPresentTarget(omr.MPresentTarget):
    def __init__(self, name):
        omr.MPresentTarget.__init__(self, name)
        
        self.mTarget = None

    def __del__(self):
        self.mTarget = None

    def targetOverrideList(self):
        if self.mTarget is not None:
            if kDebugAll:
                print ("Returning present target: %s" % self.mTarget)
            return [self.mTarget]
        return None

    def setRenderTarget(self, target):
        self.mTarget = target
