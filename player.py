import pygame
import numpy as np
from utils import crossed_wall
from bullet import Bullet


class Player:
    def __init__(self, pos: np.ndarray, angle: float):
        self.pos = pos
        self.angle = angle
        self.bullets = []

    def rotate(self, angle: float):
        self.angle += angle

    def move_forward(self, walls: list, distance: float):
        self.move(walls, distance * np.cos(self.angle), distance * np.sin(self.angle))

    def move(self, walls: list, dx: float, dy: float):
        for wall in walls:
            if crossed_wall(wall, [self.pos, self.pos + 2*np.array([dx, dy])]):
                return

        self.pos += np.array([dx, dy])

    def move_bullets(self, walls: list, players: list):
        for bullet in self.bullets:
            bullet.move(walls, players)

        self.bullets = [bullet for bullet in self.bullets if bullet.alive]

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def shoot(self):
        self.bullets.append(
            Bullet(self.pos.copy(), np.array([np.cos(self.angle), np.sin(self.angle)]))
        )

    def hit(self):
        print("I am hit!")

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 4)
        # draw a line of length 10 in the direction of the player
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (int(self.pos[0]), int(self.pos[1])),
            (
                int(self.pos[0] + 50 * np.cos(self.angle)),
                int(self.pos[1] + 50 * np.sin(self.angle)),
            ),
        )
