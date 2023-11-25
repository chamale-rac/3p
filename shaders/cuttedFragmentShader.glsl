#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform float time;

in vec2 UVs;
in vec3 outNormals;
in mat4 outViewMatrix;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(lightPos - gl_FragCoord.xyz);
    float diffuse = max(dot(outNormals, lightDir), 0.0);
    
    // Get speed based lightDir y on the scale of 0.0 to 1.0
    float speed = (lightDir.y + 1.0) / 2.0;

    // Dont paint the pixels between the stripes
    // Use a sine function to make the stripes move smoothly on y
    

    if (cos(6.0 * outPosition.y + 3.0 * speed/10 * time) < 0.0)
    {
        discard;
    }


    fragColor = vec4(diffuse * texture(tex, UVs).rgb, 1.0);
}