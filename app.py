import pygame
from pygame.locals import *
import glm
from model import Model
from shaders import fragment_shader, vertex_shader

from gl import Renderer

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock  = pygame.time.Clock()

renderer = Renderer(screen)

renderer.setShaders(vertex_shader, fragment_shader)

triangle = [
    # X, Y, Z, R, G, B
    -0.5, -0.5, 0.0, 1, 0.0, 0.0,
     0.0,  0.5, 0.0, 0.0, 1, 0.0,
     0.5, -0.5, 0.0, 0.0, 0.0, 1,
]

triangleBuffer = Model(triangle)

triangleBuffer.position.z = -10
triangleBuffer.scale = glm.vec3(3,3,3)

renderer.sceneObjects.append(triangleBuffer)


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

    if keys[K_d]:
        renderer.camPosition.x += 5 * deltaTime
    if keys[K_a]:
        renderer.camPosition.x -= 5 * deltaTime
    if keys[K_w]:
        renderer.camPosition.y += 5 * deltaTime
    if keys[K_s]:
        renderer.camPosition.y -= 5 * deltaTime
    if keys[K_q]:
        renderer.camPosition.z += 5 * deltaTime
    if keys[K_e]:
        renderer.camPosition.z -= 5 * deltaTime

    # Mouse rotation
    mouseX, mouseY = pygame.mouse.get_rel()
    renderer.camRotation.y -= mouseX * deltaTime
    renderer.camRotation.x -= mouseY * deltaTime

    # constant rotation
    # triangleBuffer.rotation.y += 45 * deltaTime

    renderer.render()
    pygame.display.flip()
    

pygame.quit()