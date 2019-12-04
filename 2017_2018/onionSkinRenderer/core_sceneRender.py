import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr

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
        super(viewRenderSceneRender,self).__init__(name, 'Onion')
        self.clearMask = clearMask
        self.panelName = ""
        self.drawSelectionFilter = False
        self.onionObjectList = om.MSelectionList()
        self.target = None
        self.sceneFilter = omr.MSceneRender.kNoSceneFilterOverride

    def __del__(self):
        self.mSelectionList = None
        self.target = None

    # draw only selected objects if drawSelectionFilter is True
    def objectSetOverride(self):
        if self.drawSelectionFilter:
            return self.onionObjectList
        return None

    # called from viewRenderOverride which manages the list
    def setObjectFilterList(self, selectionList):
        self.onionObjectList = selectionList

    # sets the clear mask
    def clearOperation(self):
        self.mClearOperation.setClearColor((0.0, 0.0, 0.0, 0.0))
        self.mClearOperation.setMask(self.clearMask)
        return self.mClearOperation

    # allows setting the draw selection filter which will only
    # draw selected objects
    def setDrawSelectionFilter(self, flag):
        self.drawSelectionFilter = flag

    def setRenderTarget(self, target):
        self.target = target

    def targetOverrideList(self):
        if self.target is not None:
            return [self.target]
        return None
    
    def setSceneFilter(self, filter):
        self.sceneFilter = filter

    def renderFilterOverride(self):
        return self.sceneFilter