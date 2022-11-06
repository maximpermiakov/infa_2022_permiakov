import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

circle(screen, (255, 255, 0), (200, 200), 150)
circle(screen, (0, 0, 0), (200, 200), 150, 1)
rect(screen, (0, 0, 0), (125, 270, 150, 30))
circle(screen, (255, 0, 0), (130, 150), 30)
circle(screen, (0, 0, 0), (130, 150), 10)
circle(screen, (0, 0, 0), (130, 150), 30, 1)
circle(screen, (255, 0, 0), (270, 150), 25)
circle(screen, (0, 0, 0), (270, 150), 10)
circle(screen, (0, 0, 0), (270, 150), 25, 1)
polygon(screen, (0, 0, 0), [(70, 85), (170, 135),
                    (180, 115), (80, 65), (70, 85)])
polygon(screen, (0, 0, 0), [(350, 40), (360, 60),
                    (210, 160), (200, 140), (350, 40)])
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()