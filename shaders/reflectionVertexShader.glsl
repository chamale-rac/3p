#version 330 core
layout (location = 0) in vec3 position;
layout (location = 2) in vec3 normal;

out vec3 outNormals;
out vec3 outPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    outNormals = mat3(transpose(inverse(modelMatrix))) * normal;
    outPosition = vec3(modelMatrix * vec4(position, 1.0));
    gl_Position = projectionMatrix * viewMatrix * vec4(outPosition, 1.0);
}  