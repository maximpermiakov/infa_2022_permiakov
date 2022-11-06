import pygame
from pygame.draw import *
from random import randint
pygame.init()

# Screen
FPS = 30
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# array of balls
balls = []

# max amount of balls
amount = 5

# score
score = 0
f1 = pygame.font.Font(None, 36)


def new_ball():
    """makes new ball, defines its velocity """
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT - 100)
    if randint(1, 100) <= 5:
        vx = randint(0, 20)
        vy = randint(0, 20)
        r = randint(5, 10)
        color = BLACK
    else:
        vx = randint(-10, 10)
        vy = randint(-10, 10)
        r = randint(10, 50)
        color = COLORS[randint(0, 5)]
    ball = [x, y, vx, vy, r, color]
    balls.append(ball)


def move_ball():
    """moves the balls """
    for ball in balls:
        ball[0] += ball[2]
        ball[1] += ball[3]


def reflect_ball():
    """makes wall reflections"""
    for ball in balls:
        if ball[0] + ball[4] >= WIDTH or ball[0] - ball[4] <= 0:
            ball[2] = - ball[2]
        if ball[1] + ball[4] >= HEIGHT or ball[1] - ball[4] <= 0:
            ball[3] = - ball[3]


def draw_ball():
    """draws the balls"""
    for ball in balls:
        circle(screen, ball[5], (ball[0], ball[1]), ball[4])


def ball_hit(mouse, coord, r):
    """Checks if mouse hit the ball
    mouse is coordinates of the event
    coord is coordinates of the ball
    r is radius of the ball"""
    return (coord[0] - mouse.pos[0]) ** 2 + (coord[1] - mouse.pos[1]) ** 2 <= r**2


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if ball_hit(event, [ball[0], ball[1]], ball[4]):
                    score += (ball[2]**2 + ball[3]**2)**0.5/ball[4]
                    balls.remove(ball)
    if len(balls) < amount:
        new_ball()
    screen.fill(WHITE)
    move_ball()
    reflect_ball()
    draw_ball()
    text1 = f1.render(str(int(round(score*100, 1))), 1, (0, 0, 0))
    screen.blit(text1, (10, 10))
    pygame.display.update()
pygame.quit()
