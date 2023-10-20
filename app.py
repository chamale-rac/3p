import pygame
from pygame.locals import *
from buffer import Buffer
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

triangleBuffer = Buffer(triangle)
renderer.sceneObjects.append(triangleBuffer)

isRunning = True
while isRunning:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False

    deltaTime = clock.tick(60) / 1000.0
    
    renderer.render()
    pygame.display.flip()

pygame.quit()