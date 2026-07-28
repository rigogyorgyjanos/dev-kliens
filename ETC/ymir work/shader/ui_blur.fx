//blackdragonx61 / Mali

texture SceneTex;

sampler2D texSampler = sampler_state
{
    Texture = <SceneTex>;
    MinFilter = LINEAR;
    MagFilter = LINEAR;
};

float BlurStrength = 0.02;

struct PS_IN
{
    float2 uv : TEXCOORD0;
};

float4 PS_BlurH(PS_IN IN) : COLOR
{
    float2 uv = IN.uv;
    float offs = BlurStrength;

    // Weights normalized to sum to 1.0 (were 1.3, which overbrightened/clipped
    // the image on every pass - visible as blown-out blocky highlights).
    float4 c = tex2D(texSampler, uv) * 0.1538;

    c += tex2D(texSampler, uv + float2(offs * 1, 0)) * 0.1385;
    c += tex2D(texSampler, uv - float2(offs * 1, 0)) * 0.1385;

    c += tex2D(texSampler, uv + float2(offs * 2, 0)) * 0.1154;
    c += tex2D(texSampler, uv - float2(offs * 2, 0)) * 0.1154;

    c += tex2D(texSampler, uv + float2(offs * 3, 0)) * 0.0769;
    c += tex2D(texSampler, uv - float2(offs * 3, 0)) * 0.0769;

    c += tex2D(texSampler, uv + float2(offs * 4, 0)) * 0.0462;
    c += tex2D(texSampler, uv - float2(offs * 4, 0)) * 0.0462;

    c += tex2D(texSampler, uv + float2(offs * 6, 0)) * 0.0308;
    c += tex2D(texSampler, uv - float2(offs * 6, 0)) * 0.0308;

    c += tex2D(texSampler, uv + float2(offs * 8, 0)) * 0.0154;
    c += tex2D(texSampler, uv - float2(offs * 8, 0)) * 0.0154;

    return c;
}


float4 PS_BlurV(PS_IN IN) : COLOR
{
    float2 uv = IN.uv;
    float offs = BlurStrength;

    // Weights normalized to sum to 1.0 (were 1.3, which overbrightened/clipped
    // the image on every pass - visible as blown-out blocky highlights).
    float4 c = tex2D(texSampler, uv) * 0.1538;

    c += tex2D(texSampler, uv + float2(0, offs * 1)) * 0.1385;
    c += tex2D(texSampler, uv - float2(0, offs * 1)) * 0.1385;

    c += tex2D(texSampler, uv + float2(0, offs * 2)) * 0.1154;
    c += tex2D(texSampler, uv - float2(0, offs * 2)) * 0.1154;

    c += tex2D(texSampler, uv + float2(0, offs * 3)) * 0.0769;
    c += tex2D(texSampler, uv - float2(0, offs * 3)) * 0.0769;

    c += tex2D(texSampler, uv + float2(0, offs * 4)) * 0.0462;
    c += tex2D(texSampler, uv - float2(0, offs * 4)) * 0.0462;

    c += tex2D(texSampler, uv + float2(0, offs * 6)) * 0.0308;
    c += tex2D(texSampler, uv - float2(0, offs * 6)) * 0.0308;

    c += tex2D(texSampler, uv + float2(0, offs * 8)) * 0.0154;
    c += tex2D(texSampler, uv - float2(0, offs * 8)) * 0.0154;

    return c;
}


technique Blur
{
    pass Horizontal
    {
        PixelShader = compile ps_2_0 PS_BlurH();
    }

    pass Vertical
    {
        PixelShader = compile ps_2_0 PS_BlurV();
    }
}