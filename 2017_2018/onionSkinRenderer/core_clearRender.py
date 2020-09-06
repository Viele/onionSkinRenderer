import maya.api.OpenMayaRender as omr

"""
fill the render with a color
"""
class viewRenderClearRender(omr.MClearOperation):
    def __init__(self, name):
        omr.MClearOperation.__init__(self, name)

        self.target = None

    def __del__(self):
        self.target = None

    def targetOverrideList(self):
        if self.target is not None:
            return [self.target]
        return None

    def setRenderTarget(self, target):
        self.target = target
