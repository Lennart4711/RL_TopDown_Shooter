import numpy as np
import pygame
import random

pygame.init()

from player import Player
from utils import crossed_wall

WIDTH = 400
HEIGHT = 400
RUNNING_SPEED = 2


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

p1 = Player(np.array([WIDTH / 4, HEIGHT / 2]), 0)
target = Player(np.array([WIDTH / 1.5, HEIGHT / 2]), 0)

running = True

walls = [
    [np.array([0, 0]), np.array([WIDTH, 0])],
    [np.array([WIDTH, 0]), np.array([WIDTH, HEIGHT])],
    [np.array([WIDTH, HEIGHT]), np.array([0, HEIGHT])],
    [np.array([0, HEIGHT]), np.array([0, 0])],
    [np.array([WIDTH / 2, HEIGHT/4]), np.array([WIDTH / 2, HEIGHT / 1.5])],
]


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

    # Rotate towards the mouse
    mouse_pos = np.array(pygame.mouse.get_pos())
    p1.rotate_towards(mouse_pos)

    if keys[pygame.K_w]:
        p1.move(walls, 0, -RUNNING_SPEED)
    if keys[pygame.K_s]:
        p1.move(walls, 0, RUNNING_SPEED)
    if keys[pygame.K_a]:
        p1.move(walls, -RUNNING_SPEED, 0)
    if keys[pygame.K_d]:
        p1.move(walls, RUNNING_SPEED, 0)

    # if mouse is pressed, shoot
    if pygame.mouse.get_pressed()[0]:
        p1.shoot()

    p1.move_bullets(walls, [])

    p1.draw(screen)
    p1.cast_ray(screen, walls, -45)
    p1.cast_ray(screen, walls, 45)#
    p1.draw_bullets(screen)
    for wall in walls:
        pygame.draw.line(screen, (255, 255, 255), wall[0], wall[1])

    FOW = np.deg2rad(90)
    # If the player can see the target, draw a line between them
    if not any(crossed_wall(wall, [p1.pos, target.pos]) for wall in walls):
        # Draw the line if the player can see the target inside a 90 degree angle
        if p1.sees_player(target, 45):
            pygame.draw.line(screen, (0, 255, 0), p1.pos, target.pos)
            target.draw(screen)


    clock.tick(60)
    pygame.display.update()

