import maya.api.OpenMayaRender as omr

"""
This displays the render in the viewport
"""
class viewRenderPresentTarget(omr.MPresentTarget):
    def __init__(self, name):
        omr.MPresentTarget.__init__(self, name)
        
        self.target = None

    def __del__(self):
        self.target = None

    def targetOverrideList(self):
        if self.target is not None:
            return [self.target]
        return None

    def setRenderTarget(self, target):
        self.target = target
