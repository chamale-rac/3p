#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform float time;
uniform float height;
uniform float width;

in vec2 UVs;
in vec3 outNormals;
in mat4 outViewMatrix;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(lightPos - gl_FragCoord.xyz);
    float diffuse = max(dot(outNormals, lightDir), 0.0);
    
    // Scale lightDir.x to the width of the screen
    float pixelRate = (lightDir.y + 1.0) / 2.0;
    float squareSize = floor(2.0 + 30.0 * (pixelRate/3));

    vec2 resolution = vec2(width, height);
    
    vec2 center = squareSize * floor(UVs * resolution / squareSize) + squareSize * vec2(0.5, 0.5);
    vec2 corner1 = center + squareSize * vec2(-0.5, -0.5);
    vec2 corner2 = center + squareSize * vec2(0.5, -0.5);
    vec2 corner3 = center + squareSize * vec2(0.5, 0.5);
    vec2 corner4 = center + squareSize * vec2(-0.5, 0.5);

    // Calc the avg color
    vec3 pixelColor = 0.4 * texture(tex, center/resolution).rgb;
    pixelColor += 0.15 * texture(tex, corner1/resolution).rgb;
    pixelColor += 0.15 * texture(tex, corner2/resolution).rgb;
    pixelColor += 0.15 * texture(tex, corner3/resolution).rgb;
    pixelColor += 0.15 * texture(tex, corner4/resolution).rgb;

    fragColor = vec4(pixelColor, 1.0);
    // fragColor = vec4(diffuse * texture(tex, UVs).rgb, 1.0);
}