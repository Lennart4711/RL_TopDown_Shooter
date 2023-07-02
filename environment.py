import tensorflow as tf
import numpy as np
from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts
from tf_agents.typing import types
from game import Game
from player import Player
from ai_player import AI_Player

from game import WIDTH, HEIGHT

SURVIVED_REWARD = 0
KILLED_ENEMY_REWARD = 100


class GameEnv(py_environment.PyEnvironment):
    def __init__(self):
        # Possible actions: change x by +-1, change y by +-1, change angle by +-1, shoot
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(4,),  # 4-dimensional action space
            dtype=np.float32,
            minimum=[-1, -1, -1, 0],  # Minimum values for each dimension
            maximum=[1, 1, 1, 1],  # Maximum values for each dimension

        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(6,),  # 6-dimensional observation space
            dtype=np.float32,
            minimum=[0, 0, 0, 0, 0, 0],  # Minimum values for each dimension
            maximum=[100, 100, 100, 400, 400, 100],  # Maximum values for each dimension
        )
        self._state = np.zeros(6)
        self._episode_ended = False
        self._reset()

    def action_spec(self) -> types.NestedArraySpec:
        return self._action_spec

    def observation_spec(self) -> types.NestedArraySpec:
        return self._observation_spec

    def _reset(self):
        self._state = np.zeros(6)
        self._episode_ended = False
        self._game = Game(
            walls=[
                [np.array([0, 0]), np.array([WIDTH, 0])],
                [np.array([WIDTH, 0]), np.array([WIDTH, HEIGHT])],
                [np.array([WIDTH, HEIGHT]), np.array([0, HEIGHT])],
                [np.array([0, HEIGHT]), np.array([0, 0])],
                [
                    np.array([WIDTH / 2, HEIGHT / 4]),
                    np.array([WIDTH / 2, HEIGHT / 1.5]),
                ],
            ],
            player1=AI_Player(np.array([WIDTH / 2, HEIGHT / 2]), 0),
            player2=Player(np.array([WIDTH / 1.9, HEIGHT / 2.2]), 0),
        )
        return ts.restart(np.array(self._state, dtype=np.float32))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        self._state = self._game.step(action)

        player_dead = False
        if self._state[0] <= 0:
            self._episode_ended = True
            reward = -KILLED_ENEMY_REWARD
            player_dead = True
        elif self._state[1] <= 0:
            self._episode_ended = True
            reward = KILLED_ENEMY_REWARD
            player_dead = True
        else:
            # reward the inflicted damage / 10
            reward = self._state[5] / 10

        if self._episode_ended or player_dead:
            # return a boundedarrayspec with the same shape as the observation spec
            print("Episode ended, reward: ", reward)
            return ts.termination(self._state, reward=float(reward))
        else:

            return ts.transition(self._state, reward=float(reward), discount=1.0)


if __name__ == "__main__":
    py_environment = GameEnv()
    utils.validate_py_environment(py_environment, episodes=5)

