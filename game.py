import numpy as np
import pygame
import time

pygame.init()

from player import Player
from human_player import HumanPlayer
from utils import crossed_wall

RUNNING_SPEED = 2
WIDTH = 400
HEIGHT = 400


class Game:
    def __init__(self, walls: list, player1: Player, player2: Player):
        self.walls = walls
        self.player1 = player1
        self.player2 = player2
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True

    # def loop(self):
    #     while self.running:
    #         self.player1.input(self.walls)

    #         self.player1.update(self.walls, self.player2, (WIDTH, HEIGHT))
    #         self.player2.update(self.walls, self.player1, (WIDTH, HEIGHT))

    #         self.clock.tick(60)
    #         self.draw()
    #         self.exit_game()
    #     pygame.quit()

    def step(self, action):
        self.player1.input(self.walls, action)
        self.player1.update(self.walls, self.player2, (WIDTH, HEIGHT))
        self.player2.update(self.walls, self.player1, (WIDTH, HEIGHT))
        self.draw()

        state = self.get_state()
        pygame.event.pump()

        return state
    

    def get_state(self):
        time_till_next_shot_ms = int(
            1000 * (max(0.1 - (time.time() - self.player1.last_shot), 0))
        )

        return np.array(
            [
                max(self.player1.health, 0),
                max(self.player2.health, 0),
                time_till_next_shot_ms,
                self.player1.enemies_last_pos[0],
                self.player1.enemies_last_pos[1],
                self.player1.inflicted_damage,
            ],
            dtype=np.float32,
        )

    def draw(self):
        self.screen.fill((0, 0, 0))

        for wall in self.walls:
            pygame.draw.line(self.screen, (255, 255, 255), wall[0], wall[1])

        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        self.draw_lines_of_sight()

        pygame.display.update()

    def exit_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_lines_of_sight(self):
        # if no walls inbetween, draw line
        if not any(
            crossed_wall(wall, [self.player1.pos, self.player2.pos])
            for wall in self.walls
        ):
            pygame.draw.line(
                self.screen, (255, 255, 255), self.player1.pos, self.player2.pos
            )

    def player_input(self):
        for player in self.players:
            player.input()

if __name__ == "__main__":
    game = Game(
        walls=[
            [np.array([0, 0]), np.array([WIDTH, 0])],
            [np.array([WIDTH, 0]), np.array([WIDTH, HEIGHT])],
            [np.array([WIDTH, HEIGHT]), np.array([0, HEIGHT])],
            [np.array([0, HEIGHT]), np.array([0, 0])],
            [np.array([WIDTH / 2, HEIGHT / 4]), np.array([WIDTH / 2, HEIGHT / 1.5])],
        ],
        player1=HumanPlayer(np.array([WIDTH / 1.5, HEIGHT / 2]), 0),
        player2=Player(np.array([WIDTH / 1.9, HEIGHT / 2.2]), 0),
    )

    game.loop()
