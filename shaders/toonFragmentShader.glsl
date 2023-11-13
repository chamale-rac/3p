#version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 lightPos;
uniform vec3 camPos;
uniform float time;

in vec2 UVs;
in vec3 outNormals;
in mat4 outViewMatrix;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    // Calculate the diffuse lighting
    vec3 lightDir = normalize(lightPos.xyz - outPosition.xyz);
    float diffuse = max(dot(outNormals, lightDir), 0.0);

    // Apply the toon shading
    float intensity = floor(diffuse * 5.0) / 5.0;

    // Apply the outline
    vec3 outlineColor = vec3(0.1, 0.1, 0.1); // Black outline color
    float outlineThickness = 0.02; // Adjust the outline thickness as needed

    vec2 texelSize = 1.0 / textureSize(tex, 0);
    for (int x = -1; x <= 1; x++) {
        for (int y = -1; y <= 1; y++) {
            vec2 offset = vec2(x, y) * outlineThickness * texelSize;
            vec4 neighborColor = texture(tex, UVs + offset);
            float neighborIntensity = dot(neighborColor.rgb, vec3(0.299, 0.587, 0.114));
            if (neighborIntensity < 0.5) {
                intensity = 1.0; // Fill outline pixels with full intensity
                break;
            }
        }
    }

    if (intensity < 0.1) {
        intensity = 0.1;
    }

    // Check the angle between the camera and the surface normal
    // if the angle is greater is around 89 and 91 degrees, the it is the outline
    // if it is the outline, then set use color white
    vec3 viewDir = normalize(outViewMatrix[3].xyz - outPosition.xyz);
    float angle = dot(outNormals, viewDir);
    // get angle always positive
    angle = abs(angle);
    if (angle > 0.20 && angle < 0.30) {
        // Instead of just using a hard color, dampen the intensity based on the angle
        // This will make the outline fade out as it approaches the edge of the model
        intensity = (1.0 - (angle - 0.10) / 0.5);
        // Now uses color yellow, and combine it with the intensity and texture color
        fragColor = vec4(intensity * vec3(1, 1, 0) + (1.0 - intensity) * outlineColor, 1.0);
    } else {
        if (intensity < 0.2) {
            intensity = 0.2;
        }
        fragColor = vec4(intensity * texture(tex, UVs).rgb * vec3(0.996, 0.203, 0.494) + (1.0 - intensity) * outlineColor, 1.0);
    }
}