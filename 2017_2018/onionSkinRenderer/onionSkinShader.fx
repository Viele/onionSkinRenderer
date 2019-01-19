// extended example "Blend" shader from the maya installation

#include "Common10.fxh"

// The source buffer and sampler
Texture2D gSourceTex < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp;

// The onion skin buffer and sampler
Texture2D gSourceTex2 < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp2;

// current onion skin to be used as a stencil to display onion skin behind mesh
Texture2D gStencilTex < string UIWidget = "None"; > = NULL;
SamplerState gStencilSampler;



// Amount to blend source
float gBlendSrc = 0.3f;
// actually don't know what that is used for. Was used in the example and doesn't break anything
float4 gUVTransform : RelativeViewportDimensions;

// viewport size in pixels to map from UV space to pixel space
float4 gPixelTransform : ViewportPixelSize;

// color with which each onion skin pixel is multiplied
float4 gTint = {0.5, 0.5, 1.0, 1.0};

// outline width in pixels
int gOutlineWidth = 5;

// sets the way the onion skin is displayed. 0 = shaded, 1 = shape, 2 = outline
uniform int gType = 0;

// defines if onion skin is drawn behind or in front of current object
// 0 = in front, 1 = behind
uniform int gDrawBehind = 1;



// Simple blending between 2 images
float4 PS_Blend(VS_TO_PS_ScreenQuad In) : SV_TARGET
{

    float4 source = gSourceTex.Sample(gSourceSamp, In.UV * gUVTransform.zw + gUVTransform.xy);
    float4 onionSource = gSourceTex2.Sample(gSourceSamp2, In.UV * gUVTransform.zw + gUVTransform.xy);
    float4 stencilSource = (gStencilTex.Sample(gStencilSampler, In.UV * gUVTransform.zw + gUVTransform.xy) * gDrawBehind -1) *-1;


    // draw shaded
    // normal blending between the original image and the buffered onion skin
    if (gType == 0) 
    {
        float4 result = float4( lerp(source, onionSource * gTint , gBlendSrc * onionSource.a * stencilSource.a));		
        return result;
    }


    // draw shape
    // uses only the alpha channel for blending, ommiting any shaded information
    else if(gType == 1)
    {
        // mult by 0.75 to darken
        float onionA = onionSource.a * 0.75f;
        float4 onionSourceAlpha = {onionA, onionA, onionA, onionA};
        float4 result = float4( lerp(source, onionSourceAlpha * gTint , gBlendSrc * onionSourceAlpha.a * stencilSource.a));		
        return result;
    }


    // draw outline
    // creates an outline around the onion skins with the thickness specified in gOutlineWidth
    else if(gType == 2)
    {
        // sample in 8 directions
        float4 onionSourceUp =          gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(0,-gOutlineWidth) / gPixelTransform.xy);
        float4 onionSourceUpLeft =      gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(gOutlineWidth/1.5,-gOutlineWidth/1.5) / gPixelTransform.xy);
        float4 onionSourceUpRight =     gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(-gOutlineWidth/1.5,-gOutlineWidth/1.5) / gPixelTransform.xy);
        float4 onionSourceDown =        gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(0,gOutlineWidth) / gPixelTransform.xy);
        float4 onionSourceDownLeft =    gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(gOutlineWidth/1.5,gOutlineWidth/1.5) / gPixelTransform.xy);
        float4 onionSourceDownRight =   gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(-gOutlineWidth/1.5,gOutlineWidth/1.5) / gPixelTransform.xy);
        float4 onionSourceLeft =        gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(gOutlineWidth,0) / gPixelTransform.xy);
        float4 onionSourceRight =       gSourceTex2.Sample(gSourceSamp2, (In.UV * gUVTransform.zw + gUVTransform.xy) + float2(-gOutlineWidth,0) / gPixelTransform.xy);

        // inverts the current alpha. That means the outline starts just outside the shape of the buffered onion skin
        // OR links all samples (+)
        float alphaCombined = onionSourceUp.a + onionSourceUpLeft.a + onionSourceUpRight.a + onionSourceDown.a + onionSourceDownLeft.a + onionSourceDownRight.a + onionSourceLeft.a + onionSourceRight.a;
        float onionLineColor = (onionSource.a-1)
            * -1
            * clamp(alphaCombined, 0.0f, 1.0f);

        float4 onionSourceLine = {onionLineColor, onionLineColor, onionLineColor, onionLineColor};

        float4 result = float4( lerp(source, onionSourceLine * gTint , gBlendSrc * onionSourceLine.a * stencilSource.a));		
        return result;
    }

    return source;
}


// The main technique.
technique10 Main
{
    pass p0
    {
		SetVertexShader(CompileShader(vs_4_0, VS_ScreenQuad()));
        SetGeometryShader(NULL);
        SetPixelShader(CompileShader(ps_4_0, PS_Blend()));
    }
}
