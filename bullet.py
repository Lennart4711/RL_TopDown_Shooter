from utils import crossed_wall
import numpy as np
import pygame


class Bullet:
    def __init__(self, pos: np.ndarray, velocity: np.ndarray, shooter_id: int):
        self.pos = pos
        self.velocity = velocity
        self.alive = True
        self.shooter = shooter_id

    def move(self, walls: list, dimensions: tuple):
        for wall in walls:
            if crossed_wall(wall, [self.pos, self.pos + self.velocity]):
                self.alive = False
                return

        self.pos += self.velocity

        if self.out_of_bounds(dimensions[0], dimensions[1]):
            self.alive = False

    def out_of_bounds(self, width, height):
        return (
            self.pos[0] < 0
            or self.pos[0] > width
            or self.pos[1] < 0
            or self.pos[1] > height
        )

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 4)
