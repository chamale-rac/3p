#version 450 core

layout (location = 0) in vec3 inPosition;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{   
    texCoords = inPosition;
    gl_Position = projectionMatrix * viewMatrix * vec4(inPosition, 1.0);
}