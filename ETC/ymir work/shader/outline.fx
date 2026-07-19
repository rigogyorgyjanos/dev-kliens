//blackdragonx61 / Mali

float4x4 WorldViewProj;
float4   Color;
float    Thickness;

struct VS_INPUT
{
	float4 Position : POSITION;
	float3 Normal   : NORMAL;
};

struct VS_OUTPUT
{
	float4 Position : POSITION;
};

VS_OUTPUT VS_Outline(VS_INPUT Input)
{
	VS_OUTPUT Output;
	float3 extrudedPos = Input.Position.xyz + (Input.Normal * Thickness);
	Output.Position = mul(float4(extrudedPos, 1.0f), WorldViewProj);
	return Output;
}

float4 PS_Outline() : COLOR
{
	return Color;
}

technique OutlineTechnique
{
	pass P0
	{
		CullMode     = CCW;
		VertexShader = compile vs_2_0 VS_Outline();
		PixelShader  = compile ps_2_0 PS_Outline();
	}
}
