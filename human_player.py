from player import Player
import numpy as np
import pygame


class HumanPlayer(Player):
    def __init__(self, pos: np.ndarray, angle: float):
        super().__init__(pos, angle)

    def input(self, walls: list):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(walls, 0, -2)
        if keys[pygame.K_s]:
            self.move(walls, 0, 2)
        if keys[pygame.K_a]:
            self.move(walls, -2, 0)
        if keys[pygame.K_d]:
            self.move(walls, 2, 0)

        # turn towards the mouse
        mouse_pos = pygame.mouse.get_pos()
        self.rotate_towards(np.array(mouse_pos))

        if pygame.mouse.get_pressed()[0]:
            self.shoot()
