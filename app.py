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
zoom_min = 15
zoom_max = 30
zoom_speed = 1.5

# Define the vertical movement limits
vertical_min = -50
vertical_max = 50

# Define the initial camera position
renderer.camPosition = glm.vec3(0, 0, radius)

# Define the initial vertical angle
vertical_angle = 0

# Define the initial zoom level
zoom = radius

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
            # Update the zoom level based on the mouse wheel movement
            zoom += event.y * zoom_speed
            zoom = max(min(zoom, zoom_max), zoom_min)

    # Get the mouse movement
    mouse_dx, mouse_dy = pygame.mouse.get_rel()

    # Update the camera's horizontal angle based on the mouse x movement
    renderer.camRotation.y += mouse_dx * deltaTime * rotationSpeed
    # Update the camera's vertical angle based on the mouse y movement

    # Update the vertical angle based on the mouse y movement
    vertical_angle += mouse_dy * deltaTime * rotationSpeed * 10
    vertical_angle = max(min(vertical_angle, vertical_max), vertical_min)

    # Calculate the camera position for circular movement
    # Calculate the camera position for circular movement
    renderer.camPosition.x = MococoAbyssgardModel.position.x + \
        radius * glm.cos(renderer.camRotation.y)
    renderer.camPosition.z = MococoAbyssgardModel.position.z + \
        radius * glm.sin(renderer.camRotation.y)
    renderer.camPosition.y = vertical_angle

    # Update the camera's position based on the zoom level
    renderer.camPosition = MococoAbyssgardModel.position + \
        (renderer.camPosition - MococoAbyssgardModel.position) * zoom / radius

    renderer.update()
    renderer.render()
    pygame.display.flip()


pygame.quit()
