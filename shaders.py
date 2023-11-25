vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    outNormals = (modelMatrix * vec4(normal, 0.0)).xyz;
    outNormals = normalize(outNormals);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
}
'''

cel_fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform float time;
uniform mat4 viewMatrix;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(lightPos - vec3(viewMatrix * vec4(UVs, texture(tex, UVs).r, 1.0)));
    float lightIntensity = max(dot(outNormals, lightDir), 0.0);
    float threshold = 0.4; // Adjust this threshold to control the cel shading effect

    vec3 celShadedColor = vec3(0.0);
    if (lightIntensity > threshold) {
        celShadedColor = vec3(1.0); // Fully lit parts will have solid color
    }

    fragColor = vec4(celShadedColor, 1.0);
}
'''


fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform float time;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{   
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

    fragColor = vec4(color1 + color2 + color3, 1.0);
}
'''

wavy_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 pos = position;
    pos.x += sin(time + pos.y) / 2;
    outNormals = (modelMatrix * vec4(normal, 0.0)).xyz;
    outNormals = normalize(outNormals);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
}
'''


fat_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float fatness;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    outNormals = (modelMatrix * vec4(normal, 0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position + outNormals * fatness;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
}
'''

light_fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    fragColor = texture(tex, UVs) * intensity;
}
'''

toon_fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);

    if (intensity < 0.3) {
        intensity = 0.3;
    } else if (intensity < 0.6) {
        intensity = 0.6;
    } else {
        intensity = 1.0;
    }

    fragColor = texture(tex, UVs) * intensity;
}
'''
