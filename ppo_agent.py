from player import Player
import numpy as np


class PPO_Player(Player):
    def __init__(self, pos: np.ndarray, angle: float):
        super().__init__(pos, angle)
        