import maya.api.OpenMayaRender as omr

DEBUG = False

"""
This class is responsible for blending onion skins on top of the viewport
Here the targets are assigned to the shader
"""
class OSQuadRender(omr.MQuadRender):
    
    kFileExtension = {
        omr.MRenderer.kOpenGL:'.cgfx',
        omr.MRenderer.kOpenGLCoreProfile: '.ogsfx',
        omr.MRenderer.kDirectX11: '.fx'
        }

    def __init__(self, name, clearMask, frame, coreInstance):

        omr.MQuadRender.__init__(self, name)

        self.shaderInstance = None

        self.mClearMask = clearMask

        self.target = None
        self.inputTarget = [None, None]
        self.stencilTarget = None

        self.frame = frame

        self.active = True

        self.tint = [1,1,1,1]

        self.opacity = 0.5

        self.coreInstance = coreInstance


        

    def __del__(self):
        if self.shaderInstance is not None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if shaderMgr is not None:
                shaderMgr.releaseShader(self.shaderInstance)
            self.shaderInstance = None
        self.target = None
        self.inputTarget = None

    def shader(self):
        if DEBUG: print("getting quad render shader")
        if not self.active:
            return None

        if self.shaderInstance is None:
            shaderMgr = omr.MRenderer.getShaderManager()
            self.shaderInstance = shaderMgr.getEffectsFileShader(
                "onionSkinShader%s"%self.kFileExtension[omr.MRenderer.drawAPI()], 
                "Main", 
                useEffectCache = False
                )
        if self.shaderInstance is not None:
            self.shaderInstance.setParameter("gSourceTex", self.inputTarget[0])
            self.shaderInstance.setParameter("gSourceTex2", self.inputTarget[1])
            self.shaderInstance.setParameter("gBlendSrc", self.opacity*self.coreInstance.globalOpacity)
            self.shaderInstance.setParameter("gTint", self.tint)
            self.shaderInstance.setParameter("gType", self.coreInstance.onionSkinDisplayType)
            self.shaderInstance.setParameter("gOutlineWidth", self.coreInstance.outlineWidth)
            self.shaderInstance.setParameter("gStencilTex", self.stencilTarget)
            self.shaderInstance.setParameter("gDrawBehind", self.coreInstance.drawBehind)

        return self.shaderInstance

    def targetOverrideList(self):
        if DEBUG: print("returning override list")
        if self.target is not None:
            return [self.target]
        return None

    def setRenderTarget(self, target):
        self.target = target

    def clearOperation(self):
        if DEBUG: print("starting clear operation")
        self.mClearOperation.setMask(self.mClearMask)
        return self.mClearOperation

    def setInputTargets(self, target1, target2):
        self.inputTarget[0] = target1
        self.inputTarget[1] = target2

    def setStencilTarget(self, stencil):
        self.stencilTarget = stencil
    
    def setActive(self, flag):
        self.active = flag

    def setTint(self, tint):
        self.tint = tint
    
    def setOpacity(self, opacity):
        self.opacity = opacity

    def setFrame(self, frame):
        self.frame = frame

