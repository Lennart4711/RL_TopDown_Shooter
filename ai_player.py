from player import Player
import numpy as np


class AI_Player(Player):
    def __init__(self, pos: np.ndarray, angle: float):
        super().__init__(pos, angle)

    def input(self, walls: list, action):
        self.move(walls, action[0], action[1])

        self.rotate(action[2])

        if action[3] >= 0.5:
            self.shoot()