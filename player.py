import pygame
import numpy as np
from utils import crossed_wall, line_line_intersection
from bullet import Bullet
import time


BULLET_SPEED = 5
BULLET_DAMAGE = 40


class Player:
    def __init__(self, pos: np.ndarray, angle: float):
        self.pos = pos
        self.angle = angle
        self.bullets = []
        self.last_shot = 0
        self.health = 100
        self.id = id(self)
        self.bullets = []


    def rotate(self, angle_degrees: float):
        self.angle += angle_degrees

        if self.angle > np.pi:
            self.angle -= 2 * np.pi
        elif self.angle < -np.pi:
            self.angle += 2 * np.pi

    def rotate_towards(self, target: np.ndarray, speed=0.5):
        # calculate the angle between the player and the target
        target_angle = np.arctan2(target[1] - self.pos[1], target[0] - self.pos[0])
        # calculate the difference between the target angle and the player angle
        angle_difference = target_angle - self.angle
        # make sure the angle difference is between -pi and pi
        angle_difference = (angle_difference + np.pi) % (2 * np.pi) - np.pi
        # rotate the player towards the target
        self.rotate(np.sign(angle_difference) * min(speed, abs(angle_difference)))

    def move(self, walls: list, dx: float, dy: float):
        for wall in walls:
            if crossed_wall(wall, [self.pos, self.pos + 2 * np.array([dx, dy])]):
                return

        self.pos += np.array([dx, dy])

    def shoot(self):
        if time.time() - self.last_shot < 0.1:
            return

        self.last_shot = time.time()

        self.bullets.append(
            Bullet(
                self.pos.copy(),
                np.array([np.cos(self.angle), np.sin(self.angle)]) * BULLET_SPEED,
                self.id,
            )
        )

    def move_bullets(self, walls: list, players: list):
        for bullet in self.bullets:
            bullet.move(walls, players)

        self.bullets = [bullet for bullet in self.bullets if bullet.alive]

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def hit(self):
        self.health -= BULLET_DAMAGE

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
        for bullet in self.bullets:
            bullet.draw(screen)

    def player_in_fow(self, target_player, n):
        # Calculate the vector from the player to the target
        player_to_target = np.array(target_player.pos) - np.array(self.pos)

        # Calculate the normalized vector in the direction of the player's angle
        player_direction = np.array([np.cos(self.angle), np.sin(self.angle)])

        # Calculate the cosine of the angle between the two vectors
        cosine_angle = np.dot(player_to_target, player_direction) / (
            np.linalg.norm(player_to_target) * np.linalg.norm(player_direction)
        )

        # Calculate the angle in degrees
        angle_degrees = np.arccos(cosine_angle) * 180 / np.pi

        # Check if the angle is less than n degrees
        if angle_degrees < n:
            return True
        else:
            return False

    def input(self, walls, enemy, dimensions):
        pass

    def update(self, walls, enemy, dimensions):
        for bullet in self.bullets:
            bullet.move(walls, dimensions)
            if bullet.out_of_bounds(dimensions[0], dimensions[1]):
                bullet.alive = False
            if np.linalg.norm(bullet.pos - enemy.pos) < 10:
                bullet.alive = False
                enemy.hit()
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        

