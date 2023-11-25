#version 330 core
out vec4 fragColor;


in vec3 outNormals;
in vec3 outPosition;

uniform vec3 camPos;
uniform samplerCube skybox;

void main()
{             
    float ratio = 1.00 / 1.52;
    vec3 I = normalize(outPosition - camPos);
    vec3 R = refract(I, normalize(outNormals), ratio);
    fragColor = vec4(texture(skybox, R).rgb, 1.0);
}