import numpy as np
import pygame
import random

pygame.init()

from player import Player

WIDTH = 800
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

p1 = Player(np.array([WIDTH / 2, HEIGHT / 2]), 0)

running = True

walls = [
    [np.array([0, 0]), np.array([WIDTH, 0])],
    [np.array([WIDTH, 0]), np.array([WIDTH, HEIGHT])],
    [np.array([WIDTH, HEIGHT]), np.array([0, HEIGHT])],
    [np.array([0, HEIGHT]), np.array([0, 0])],
    [np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH / 2, HEIGHT / 2 + 100])],
]

for _ in range(10):
    x1 = random.randint(0, WIDTH)
    y1 = random.randint(0, HEIGHT)
    x2 = random.randint(0, WIDTH)
    y2 = random.randint(0, HEIGHT)

    walls.append([np.array([x1, y1]), np.array([x2, y2])])



while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if a or d is pressed, rotate player1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        p1.rotate(-0.1)
    if keys[pygame.K_d]:
        p1.rotate(0.1)

    # if w or s is pressed, move player1
    if keys[pygame.K_w]:
        p1.move_forward(walls, 2)

    if keys[pygame.K_SPACE]:
        p1.shoot()

    p1.move_bullets(walls, [])

    p1.draw(screen)
    p1.draw_bullets(screen)
    for wall in walls:
        pygame.draw.line(screen, (255, 255, 255), wall[0], wall[1])

    clock.tick(60)
    pygame.display.update()
