import pygame
from pygame.locals import *
import glm
from model import Model
from object import ObjectLoader
from shaders import fragment_shader, vertex_shader

from gl import Renderer

width = 1920
height = 1080

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)

renderer.setShaders(vertex_shader, fragment_shader)

loader = ObjectLoader()

chickenObject = loader.loadObject("./assets/models/chicken.obj")
chickenModel = Model(chickenObject)
loader.cleanUp()
chickenModel.loadTexture("./assets/textures/chicken_base.png")

chickenModel.position.z = -24
chickenModel.scale = glm.vec3(2, 2, 2)
chickenModel.rotation.y = -45

renderer.sceneObjects.append(chickenModel)

obeliskObject = loader.loadObject("./assets/models/obelisk.obj")
obeliskModel = Model(obeliskObject)
loader.cleanUp()
obeliskModel.loadTexture("./assets/textures/obelisk_base.png")

obeliskModel.position.z = -20
obeliskModel.position.y = -2
obeliskModel.rotation.x = 20
obeliskModel.scale = glm.vec3(3, 3, 3)

renderer.sceneObjects.append(obeliskModel)

renderer.camPosition = glm.vec3(-17.5,        0.885,       -0.345)
renderer.camRotation = glm.vec3(12.3,      -44.506,            0)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

isRunning = True
while isRunning:
    keys = pygame.key.get_pressed()

    deltaTime = clock.tick(60) / 1000.0

    # Set window title to current FPS
    pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False
        # control + c then print camPosition and camRotation
        if event.type == KEYDOWN and event.key == K_c and keys[K_LCTRL]:
            print(f"camPosition: {renderer.camPosition}")
            print(f"camRotation: {renderer.camRotation}")

    if keys[K_d]:
        renderer.camPosition.x += 5 * deltaTime
    if keys[K_a]:
        renderer.camPosition.x -= 5 * deltaTime
    if keys[K_q]:
        renderer.camPosition.y += 5 * deltaTime
    if keys[K_e]:
        renderer.camPosition.y -= 5 * deltaTime
    if keys[K_s]:
        renderer.camPosition.z += 5 * deltaTime
    if keys[K_w]:
        renderer.camPosition.z -= 5 * deltaTime

    mouseX, mouseY = pygame.mouse.get_rel()
    renderer.camRotation.y -= mouseX * deltaTime
    renderer.camRotation.x -= mouseY * deltaTime

    # constant rotation
    # triangleBuffer.rotation.y += 45 * deltaTime

    renderer.render()
    pygame.display.flip()


pygame.quit()
