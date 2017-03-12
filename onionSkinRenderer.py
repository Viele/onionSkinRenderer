import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaAnim as oma
import maya.api.OpenMayaUI as omui
import pymel.core as pm

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
"""


"""
Constants
When M is so unhappy with your work that it refuses it,
start here to see whats wrong
"""
kDebugAll = False
kDebugRenderOverride = False
kDebugSceneRender = False
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
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "Lendenfeld", "0.1", "Any")
    try:
        global viewRenderOverrideInstance
        viewRenderOverrideInstance = viewRenderOverride("onionSkinRenderer")
        omr.MRenderer.registerOverride(viewRenderOverrideInstance)
        plugin.registerCommand(
            addOnionFrameCMD.kCommandName,
            addOnionFrameCMD.cmdCreator,
            addOnionFrameCMD.syntaxCreator
        )
        plugin.registerCommand(
            removeOnionFrameCMD.kCommandName,
            removeOnionFrameCMD.cmdCreator,
            removeOnionFrameCMD.syntaxCreator
        )
        plugin.registerCommand(
            addOnionObjectCMD.kCommandName,
            addOnionObjectCMD.cmdCreator,
            addOnionObjectCMD.syntaxCreator
        )
        plugin.registerCommand(
            removeOnionObjectCMD.kCommandName,
            removeOnionObjectCMD.cmdCreator,
            removeOnionObjectCMD.syntaxCreator
        )
        plugin.registerCommand(
            addSelectedAsOnionCMD.kCommandName,
            addSelectedAsOnionCMD.cmdCreator,
            addSelectedAsOnionCMD.syntaxCreator
        )
        plugin.registerCommand(
            removeSelectedFromOnionCMD.kCommandName,
            removeSelectedFromOnionCMD.cmdCreator,
            removeSelectedFromOnionCMD.syntaxCreator
        )
        plugin.registerCommand(
            setRelativeOnionDisplayCMD.kCommandName,
            setRelativeOnionDisplayCMD.cmdCreator,
            setRelativeOnionDisplayCMD.syntaxCreator
        )
        plugin.registerCommand(
            getOnionListCMD.kCommandName,
            getOnionListCMD.cmdCreator,
            getOnionListCMD.syntaxCreator
        )
    except:
        raise Exception("Failed to register plugin %s" % kPluginName)

# un-init
def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        global viewRenderOverrideInstance
        if viewRenderOverrideInstance is not None:
            omr.MRenderer.deregisterOverride(viewRenderOverrideInstance)
            viewRenderOverrideInstance = None
            plugin.deregisterCommand(addOnionFrameCMD.kCommandName)
            plugin.deregisterCommand(removeOnionFrameCMD.kCommandName)
            plugin.deregisterCommand(addOnionObjectCMD.kCommandName)
            plugin.deregisterCommand(removeOnionObjectCMD.kCommandName)
            plugin.deregisterCommand(addSelectedAsOnionCMD.kCommandName)
            plugin.deregisterCommand(removeSelectedFromOnionCMD.kCommandName)
            plugin.deregisterCommand(setRelativeOnionDisplayCMD.kCommandName)
            plugin.deregisterCommand(getOnionListCMD.kCommandName)
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
        omr.MRenderOverride.__init__(self, name)
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
        self.mOnionTargets = {}
        # sometimes M doesn't want to see onions,
        # thats when this should be False
        self.mEnableBlend = False
        # remember which onions M wants you to display
        self.mDisplayOnions = {}
        # Usually display onions depending on the current time,
        # but sometimes it's nice to have them absolute
        self.mRelativeOnionDisplay = True
        # save all the objects to display in a list
        self.mOnionObjectList = om.MSelectionList()
        # store the render operations that combine onions in a list
        self.mRenderOperations = []

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

    # specify that openGl and Directx11 are supported
    def supportedDrawAPIs(self):
        return (
            omr.MRenderer.kOpenGL |
            omr.MRenderer.kOpenGLCoreProfile |
            omr.MRenderer.kDirectX11
        )

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
        if self.mCurrentFrame not in self.mOnionTargets:
            self.mOnionTargets[self.mCurrentFrame] = self.mTargetMgr.acquireRenderTarget(self.mOnionTargetDescr)
        else:
            self.mOnionTargets.get(self.mCurrentFrame).updateDescription(self.mOnionTargetDescr)
        # then set the render target to the appropriate onion
        self.mOnionPass.setRenderTarget(self.mOnionTargets.get(self.mCurrentFrame))
        # set the filter list to the onion renderer
        self.mOnionPass.setObjectFilterList(self.mOnionObjectList)

        # iterating over all blend passes and setting the targets
        for blend in self.mDisplayOnions:
            blendPass = self.mDisplayOnions[blend]
            if self.mRelativeOnionDisplay:
                targetFrame = blendPass.mFrame + self.mCurrentFrame
            else:
                targetFrame = blendPass.mFrame
            if targetFrame in self.mOnionTargets:
                blendPass.setActive(True)
                blendPass.setInputTargets(self.mStandardTarget, self.mOnionTargets[targetFrame])
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

    # called by maya. Sets the name in the "Renderers" dropdown
    def uiName(self):
        return self.mUIName
    
    #
    def addDisplayOnion(self, frame):
        if frame not in self.mDisplayOnions:
            self.mDisplayOnions[frame] = viewRenderQuadRender(
                "blendPass%s" % frame,
                omr.MClearOperation.kClearNone,
                frame
            )
            self.mDisplayOnions[frame].setShader(viewRenderQuadRender.kSceneBlend)
            self.mDisplayOnions[frame].setRenderTarget(self.mStandardTarget)

            self.mRenderOperations.insert(
                self.mRenderOperations.index(self.mOnionPass) + 1,
                self.mDisplayOnions[frame]
            )
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def removeDisplayOnion(self, frame):
        if frame in self.mDisplayOnions:
            renderPass = self.mDisplayOnions.pop(frame, None)
            self.mRenderOperations.remove(renderPass)
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def addOnionObject(self, obj):
        self.mOnionObjectList.add(obj)
        self.rotOnions()

    #
    def removeOnionObject(self, obj):
        tmpList = om.MSelectionList()
        tmpList.add(obj)
        self.mOnionObjectList.merge(tmpList, om.MSelectionList.kRemoveFromList)
        self.rotOnions()

    #
    def addSelectedAsOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.mOnionObjectList.merge(selList)
        self.rotOnions()

    #
    def removeSelectedFromOnion(self):
        selList = om.MGlobal.getActiveSelectionList()
        if not selList.isEmpty():
            self.mOnionObjectList.merge(selList, om.MSelectionList.kRemoveFromList)
        self.rotOnions()

    #
    def rotOnions(self):
        if self.mTargetMgr is not None:
            for target in self.mOnionTargets:
                self.mTargetMgr.releaseRenderTarget(self.mOnionTargets.get(target))
        self.mOnionTargets.clear()
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)

    #
    def setRelativeOnionDisplay(self, flag):
        self.mRelativeOnionDisplay = flag
        omui.M3dView.refresh(omui.M3dView.active3dView(), all=True)



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
        omr.MSceneRender.__init__(self, name)
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
        if kDebugAll:
            print ("Setting up shader")
        if not self.mActive:
            return None

        if self.mShaderInstance is None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if self.mShader == self.kSceneBlend:
                # other technique would be Main
                self.mShaderInstance = shaderMgr.getEffectsFileShader("Blend", "Add")
        if self.mShaderInstance is not None:
            if kDebugAll:
                print ("Blend target 1: %s" % self.mInputTarget[0])
                print ("Blend target 2: %s" % self.mInputTarget[1])
            self.mShaderInstance.setParameter("gSourceTex", self.mInputTarget[0])
            self.mShaderInstance.setParameter("gSourceTex2", self.mInputTarget[1])
            self.mShaderInstance.setParameter("gBlendSrc", 0.1)

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

"""
Unfortunately you can't talk to M directly,
If she requires onions she will call this command
"""
class addOnionFrameCMD(om.MPxCommand):
    kCommandName = "addOnionFrame"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            frame = argData.commandArgumentInt(0)
            viewRenderOverrideInstance.addDisplayOnion(frame)

    @classmethod
    def cmdCreator(cls):
        return addOnionFrameCMD()
    
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kDouble)
        return syntax

"""
"""
class removeOnionFrameCMD(om.MPxCommand):
    kCommandName = "removeOnionFrame"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            frame = argData.commandArgumentInt(0)
            viewRenderOverrideInstance.removeDisplayOnion(frame)

    @classmethod
    def cmdCreator(cls):
        return removeOnionFrameCMD()
    
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kDouble)
        return syntax

"""
"""
class addOnionObjectCMD(om.MPxCommand):
    kCommandName = "addOnionObject"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            obj = argData.commandArgumentString(0)
            viewRenderOverrideInstance.addOnionObject(obj)

    @classmethod
    def cmdCreator(cls):
        return addOnionObjectCMD()
    
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kString)
        return syntax

"""
"""
class removeOnionObjectCMD(om.MPxCommand):
    kCommandName = "removeOnionObject"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            obj = argData.commandArgumentString(0)
            viewRenderOverrideInstance.removeOnionObject(obj)

    @classmethod
    def cmdCreator(cls):
        return removeOnionObjectCMD()
    
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kString)
        return syntax

                      
"""
"""
class addSelectedAsOnionCMD(om.MPxCommand):
    kCommandName = "addSelectedAsOnion"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            viewRenderOverrideInstance.addSelectedAsOnion()

    @classmethod
    def cmdCreator(cls):
        return addSelectedAsOnionCMD()

    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.kNoArg
        return syntax


"""
"""
class removeSelectedFromOnionCMD(om.MPxCommand):
    kCommandName = "removeSelectedFromOnion"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            viewRenderOverrideInstance.removeSelectedFromOnion()

    @classmethod
    def cmdCreator(cls):
        return removeSelectedFromOnionCMD()

    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.kNoArg
        return syntax

"""
"""
class setRelativeOnionDisplayCMD(om.MPxCommand):
    kCommandName = "setRelativeOnionDisplay"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            obj = argData.commandArgumentBool(0)
            viewRenderOverrideInstance.setRelativeOnionDisplay(obj)

    @classmethod
    def cmdCreator(cls):
        return setRelativeOnionDisplayCMD()

    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kBoolean)
        return syntax


"""
"""
class getOnionListCMD(om.MPxCommand):
    kCommandName = "getOnionList"
    kListType = "t"
    kListTypeLong = "listType"

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            pass
        else:
            global viewRenderOverrideInstance
            self.clearResult()
            if argData.isFlagSet(getOnionListCMD.kListType):
                listType = argData.flagArgumentInt(getOnionListCMD.kListType, 0)
                if listType is 0:
                    objectList = viewRenderOverrideInstance.mOnionObjectList.getSelectionStrings()
                    self.setResult(objectList)
                else:
                    frameList = viewRenderOverrideInstance.mDisplayOnions.keys()
                    self.setResult(frameList)
        
    @classmethod
    def cmdCreator(cls):
        return getOnionListCMD()

    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addFlag(
            getOnionListCMD.kListType,
            getOnionListCMD.kListTypeLong,
            om.MSyntax.kDouble
        )
        return syntax