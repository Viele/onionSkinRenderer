import maya.api.OpenMayaRender as omr

"""
adding hud elements
"""
class viewRenderHUDRender(omr.MHUDRender):
    def __init__(self):
        omr.MHUDRender.__init__(self)

        self.target = None

    def __del__(self):
        self.target = None

    def targetOverrideList(self):
        if self.target is not None:
            return [self.target]
        return None

    def setRenderTarget(self, target):
        self.target = target