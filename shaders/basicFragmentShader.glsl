#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform float time;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(lightPos - gl_FragCoord.xyz);
    float diffuse = max(dot(outNormals, lightDir), 0.0);
    // min 0.1 and max 0.9
    diffuse = diffuse * 0.4 + 0.5;
    fragColor = vec4(diffuse * texture(tex, UVs).rgb, 1.0);
}