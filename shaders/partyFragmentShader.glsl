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

    float theta = time * 1.0;

    vec3 dir1 = vec3(cos(theta), 0.0, sin(theta));
    vec3 dir2 = vec3(sin(theta), 0.0, cos(theta));
    vec3 dir3 = vec3(0.0, cos(theta), sin(theta));


    float diffuse1 = pow(dot(outNormals, dir1), 2.0);
    float diffuse2 = pow(dot(outNormals, dir2), 2.0);
    float diffuse3 = pow(dot(outNormals, dir3), 2.0);
    
    vec3 color1 = diffuse1 * vec3(1.0, 0.0, 0.0);
    vec3 color2 = diffuse2 * vec3(0.0, 0.0, 1.0);
    vec3 color3 = diffuse3 * vec3(0.0, 1.0, 0.0);

    fragColor = texture(tex, UVs) * vec4(diffuse * (color1 + color2 + color3), 1.0);
}