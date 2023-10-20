import pygame
from pygame.locals import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock  = pygame.time.Clock()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False

    deltaTime = clock.tick(60) / 1000.0
    pygame.display.flip()

pygame.quit()