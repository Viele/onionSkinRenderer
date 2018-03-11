// extended example "Blend" shader from the maya installation

#include "Common10.fxh"

// The source buffer and sampler
Texture2D gSourceTex < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp;

// The 2nd buffer and sampler
Texture2D gSourceTex2 < string UIWidget = "None"; > = NULL;
SamplerState gSourceSamp2;

// Amount to blend source
float gBlendSrc = 0.3f;
float4 gUVTransform : RelativeViewportDimensions;
float4 gTint = {0.5, 0.5, 1.0, 1.0};

// Simple blending between 2 images
float4 PS_Blend(VS_TO_PS_ScreenQuad In) : SV_TARGET
{
    float4 source = gSourceTex.Sample(gSourceSamp, In.UV * gUVTransform.zw + gUVTransform.xy);
    float4 source2 = gSourceTex2.Sample(gSourceSamp2, In.UV * gUVTransform.zw + gUVTransform.xy);
	float4 result = float4( lerp(source, source2 * gTint , gBlendSrc * source2.a));		
    return result;
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
