import maya.api.OpenMayaRender as omr

"""
M doesn't want to see only onions, but also the surrounding veggies.
With this tool, you can combine displays so you can show them at
the same time
"""
class viewRenderQuadRender(omr.MQuadRender):
    kEffectNone = 0
    kSceneBlend = 1
    
    kFileExtension = {
        omr.MRenderer.kOpenGL:'.cgfx',
        omr.MRenderer.kOpenGLCoreProfile: '.ogsfx',
        omr.MRenderer.kDirectX11: '.fx'
        }

    def __init__(self, name, clearMask, frame):

        omr.MQuadRender.__init__(self, name)

        self.shaderInstance = None

        self.clearMask = clearMask

        self.target = None
        self.inputTarget = [None, None]
        self.stencilTarget = None

        self.shader = self.kEffectNone

        self.frame = frame

        self.active = True

        self.tint = [1,1,1,1]

        self.opacity = 0.5


        

    def __del__(self):
        if self.shaderInstance is not None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if shaderMgr is not None:
                shaderMgr.releaseShader(self.shaderInstance)
            self.shaderInstance = None
        self.target = None
        self.inputTarget = None

    def shader(self):
        if not self.active:
            return None

        if self.shaderInstance is None:
            shaderMgr = omr.MRenderer.getShaderManager()
            if self.shader == self.kSceneBlend:
                self.shaderInstance = shaderMgr.getEffectsFileShader(
                    "onionSkinShader%s"%self.kFileExtension[omr.MRenderer.drawAPI()], 
                    "Main", 
                    useEffectCache = not kDebugQuadRender
                    )
        if self.shaderInstance is not None:
            self.shaderInstance.setParameter("gSourceTex", self.inputTarget[0])
            self.shaderInstance.setParameter("gSourceTex2", self.inputTarget[1])
            self.shaderInstance.setParameter("gBlendSrc", self.opacity*viewRenderOverrideInstance.mGlobalOpacity)
            self.shaderInstance.setParameter("gTint", self.tint)
            self.shaderInstance.setParameter("gType", viewRenderOverrideInstance.mOnionType)
            self.shaderInstance.setParameter("gOutlineWidth", viewRenderOverrideInstance.mOutlineWidth)
            self.shaderInstance.setParameter("gStencilTex", self.stencilTarget)
            self.shaderInstance.setParameter("gDrawBehind", viewRenderOverrideInstance.mDrawBehind)

        return self.shaderInstance

    def targetOverrideList(self):
        if self.target is not None:
            return [self.target]
        return None

    def setRenderTarget(self, target):
        self.target = target

    def clearOperation(self):
        self.mClearOperation.setMask(self.clearMask)
        return self.mClearOperation

    def setShader(self, shader):
        self.shader = shader

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

