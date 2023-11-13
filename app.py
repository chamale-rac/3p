import pygame
from pygame.locals import *  # type: ignore
import glm
from model import Model
from object import ObjectLoader
from shaders import fragment_shader, vertex_shader, cel_fragment_shader

from gl import Renderer

width = 1080
height = 720

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)

renderer.setShaders('./shaders/basicVertexShader.glsl',
                    './shaders/basicFragmentShader.glsl')

loader = ObjectLoader()


MococoAbyssgardObj = loader.loadObject("./assets/models/MococoAbyssgard.obj")
MococoAbyssgardModel = Model(MococoAbyssgardObj)  # type: ignore
loader.cleanUp()

MococoAbyssgardModel.loadTexture("./assets/textures/MococoAbyssgard.png")
MococoAbyssgardModel.position.z = -15
MococoAbyssgardModel.position.y = -5
MococoAbyssgardModel.scale = glm.vec3(3, 3, 3)

renderer.sceneObjects.append(MococoAbyssgardModel)
renderer.target.z = -15
renderer.target.y = 0

renderer.lightPos = glm.vec3(1052, 0, 401)

pygame.mouse.set_visible(True)
pygame.event.set_grab(False)

isRunning = True

rotationSpeed = 1

# Define the radius of the circular movement and the zoom limits
radius = 30
zoom_min = 3
zoom_max = 30
zoom_speed = 1.5

# Define the vertical movement limits
vertical_min = -4.5
vertical_max = 4.4

# Define the initial camera position
renderer.camPosition = glm.vec3(0, 0, radius)

# Define the initial vertical angle
vertical_angle = 0

# Define the initial zoom level
zoom = radius
# Initialize momentum
momentum_y = 0.0
momentum_vertical = 0.0
momentum_decrease = 0.05
light_radius = 401
light_rotation_speed = 2  # Adjust the rotation speed as needed


def rotate_point(x, y, cx, cy, angle):
    """Rotate a point (x, y) around a center (cx, cy) by a given angle (in radians)."""
    dx = x - cx
    dy = y - cy
    new_x = cx + dx * glm.cos(angle) - dy * glm.sin(angle)
    new_y = cy + dx * glm.sin(angle) + dy * glm.cos(angle)
    return new_x, new_y


while isRunning:
    keys = pygame.key.get_pressed()

    deltaTime = clock.tick(60) / 1000.0

    # Set window title to current FPS
    pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

    # update elapsedTime
    renderer.elapsedTime += deltaTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False
        if event.type == KEYDOWN and event.key == K_f:
            renderer.toggleFillMode()
        if event.type == MOUSEWHEEL:
            zoom_speed = zoom / radius
            zoom += event.y * zoom_speed * deltaTime * 35
            zoom = max(min(zoom, zoom_max), zoom_min)

    if keys[K_1]:
        renderer.setShaders('./shaders/basicVertexShader.glsl',
                            './shaders/basicFragmentShader.glsl')
    if keys[K_2]:
        renderer.setShaders('./shaders/basicVertexShader.glsl',
                            './shaders/partyFragmentShader.glsl')
    if keys[K_3]:
        renderer.setShaders('./shaders/basicVertexShader.glsl',
                            './shaders/toonFragmentShader.glsl')
    if keys[K_4]:
        renderer.setShaders('./shaders/basicVertexShader.glsl',
                            './shaders/cuttedFragmentShader.glsl')
    if keys[K_5]:
        renderer.setShaders('./shaders/basicVertexShader.glsl',
                            './shaders/pixelateFragmentShader.glsl')

    # damp rotation speed based on zoom level
    rotationSpeed = zoom / radius
    maxRotationSpeed = 1.5
    rotationSpeed = min(rotationSpeed, maxRotationSpeed)

    # Get the mouse movement
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        # Update momentum along with camRotation.y and vertical_angle
        momentum_y += mouse_dx / 10 * deltaTime * rotationSpeed
        momentum_vertical += mouse_dy / 10 * deltaTime * rotationSpeed * 2
    else:
        # Decrease momentum
        momentum_y *= (1 - momentum_decrease)
        momentum_vertical *= (1 - momentum_decrease)
    maxMomentum = 0.25
    # momentum_y must be in range [-maxMomentum, maxMomentum]
    momentum_y = max(min(momentum_y, maxMomentum), -maxMomentum)

    # Add momentum to camRotation.y and vertical_angle
    renderer.camRotation.y += momentum_y
    vertical_angle += momentum_vertical
    vertical_angle = max(min(vertical_angle, vertical_max), vertical_min)

    # Calculate the camera position for circular movement
    # Calculate the camera position for circular movement
    renderer.camPosition.x = MococoAbyssgardModel.position.x + \
        radius * glm.cos(renderer.camRotation.y)
    renderer.camPosition.z = MococoAbyssgardModel.position.z + \
        radius * glm.sin(renderer.camRotation.y)

    renderer.target.y = vertical_angle
    renderer.camPosition.y = vertical_angle

    renderer.camPosition.x = MococoAbyssgardModel.position.x + \
        (renderer.camPosition.x - MococoAbyssgardModel.position.x) * zoom / radius
    renderer.camPosition.z = MococoAbyssgardModel.position.z + \
        (renderer.camPosition.z - MococoAbyssgardModel.position.z) * zoom / radius

    if keys[K_a]:
        # Rotate the light position around the model
        renderer.lightPos.x, renderer.lightPos.y = rotate_point(
            renderer.lightPos.x, renderer.lightPos.y, MococoAbyssgardModel.position.x, MococoAbyssgardModel.position.y, light_rotation_speed * deltaTime)
    if keys[K_d]:
        renderer.lightPos.x, renderer.lightPos.y = rotate_point(
            renderer.lightPos.x, renderer.lightPos.y, MococoAbyssgardModel.position.x, MococoAbyssgardModel.position.y, -light_rotation_speed * deltaTime)
    if keys[K_w]:
        renderer.lightPos.x, renderer.lightPos.z = rotate_point(
            renderer.lightPos.x, renderer.lightPos.z, MococoAbyssgardModel.position.x, MococoAbyssgardModel.position.z, light_rotation_speed * deltaTime)
    if keys[K_s]:
        renderer.lightPos.x, renderer.lightPos.z = rotate_point(
            renderer.lightPos.x, renderer.lightPos.z, MococoAbyssgardModel.position.x, MococoAbyssgardModel.position.z, -light_rotation_speed * deltaTime)

    renderer.update()
    renderer.render()
    pygame.display.flip()


pygame.quit()

# TODO: enable or disable damping
# TODO: enable or disable mouse visibility
# TODO: enable or disable automatic rotation model
