import pygame
from pygame.locals import *
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

rotationSpeed = 20

autoRotate = False

isRunning = True
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
        # R enable or disable auto rotation
        if event.type == KEYDOWN and event.key == K_r:
            autoRotate = not autoRotate
        # Z reset light position x and y
        if event.type == KEYDOWN and event.key == K_z:
            renderer.lightPos.x = 1052
            renderer.lightPos.y = 0

    # Change shaders based on key pressed 1, 2, 3...
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

    if autoRotate:
        MococoAbyssgardModel.rotation.y += deltaTime * rotationSpeed

    if keys[K_a]:
        MococoAbyssgardModel.rotation.y -= deltaTime * rotationSpeed * 4
    if keys[K_d]:
        MococoAbyssgardModel.rotation.y += deltaTime * rotationSpeed * 4

    if keys[K_UP]:
        rotationSpeed += 4
    if keys[K_DOWN]:
        rotationSpeed -= 4

    # Use mouse position to
    mouse_x, mouse_y = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        renderer.lightPos.x += mouse_x * 3
        renderer.lightPos.y -= mouse_y * 3

    renderer.update()
    renderer.render()
    pygame.display.flip()


pygame.quit()
