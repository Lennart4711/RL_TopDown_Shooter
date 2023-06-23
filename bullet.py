from utils import crossed_wall
import numpy as np
import pygame


class Bullet:
    def __init__(self, pos: np.ndarray, velocity: np.ndarray):
        self.pos = pos
        self.velocity = velocity
        self.alive = True

    def move(self, walls: list, players: list):
        for wall in walls:
            if crossed_wall(wall, [self.pos, self.pos + self.velocity]):
                self.alive = False
                return

        for player in players:
            if np.linalg.norm(self.pos - player.pos) < 10:
                self.alive = False
                player.hit()

        self.pos += self.velocity

        if self.out_of_bounds(800, 800):
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
