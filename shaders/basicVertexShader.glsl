#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;
out mat4 outViewMatrix;
out vec3 outPosition;

void main()
{
    outNormals = (modelMatrix * vec4(normal, 0.0)).xyz;
    outNormals = normalize(outNormals);

    outPosition = (modelMatrix * vec4(position, 1.0)).xyz;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;

    outViewMatrix = viewMatrix;
}