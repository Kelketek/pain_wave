# PLAY US A GAME! :V
from math import floor
from random import random

import pygame
import sys

from src.entity import Entity
from src.physics import Position, Movement, update_movement, update_collisions, Collision
from src.boundary import update_boundary
from src.friction import update_friction, Friction


def get_joysticks():
    return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


DEAD_ZONE = .1


def normalize_axis(value):
    if 0 < value < DEAD_ZONE:
        value = 0
    if DEAD_ZONE > value > 0:
        value = 0
    if value:
        if value > 0:
            value -= DEAD_ZONE
        else:
            value += DEAD_ZONE
    value *= 100
    value /= 15
    return floor(value)


DIRECT_MAP = {
    pygame.K_w: (0, -3),
    pygame.K_a: (-3, 0),
    pygame.K_s: (0, 3),
    pygame.K_d: (3, 0)
}

# Desired framerate in frames per second. Try out other values.
FPS = 30

BLACK = 0, 0, 0
NOT_QUITE_BLACK = 22, 22, 22
RED = 255, 0, 0


class Image:
    def __init__(self, path, position, depth=0):
        self.image = pygame.transform.scale(
            pygame.image.load(path),
            (floor(position.radius * 2), floor(position.radius * 2))
        )
        self.position = position

    def blit(self, screen):
        rect = (
            floor(self.position.x - self.position.radius), floor(self.position.y - self.position.radius),
            floor(self.position.x + self.position.radius), floor(self.position.y - self.position.radius)
        )
        screen.blit(self.image, rect)


class PainWave:
    def __init__(self, width=600, height=600):
        pygame.init()
        pygame.joystick.init()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(0)
        self.size = self.width, self.height = width, height
        self.playtime = 0.0
        self.offset = 0
        self.moved = False

        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWACCEL)
        self.ball = pygame.image.load("assets/ball.gif")
        self.ball_rect = self.ball.get_rect()
        pygame.joystick.init()
        self.entities = []
        self.joystick_list = []
        self.player_dict = {}

        for _ in range(10):
            entity = Entity()
            self.entities.append(entity)
            entity.add(Position(random() * 250, random() * 250, random() * 12 + 8))
            entity.add(Movement())
            entity.add(Collision(random() * 10 + 40))
            entity.add(Friction(.9))

    @property
    def players(self):
        if len(self.player_dict) == len(self.joysticks):
            return self.player_dict
        for joystick in self.joysticks:
            if joystick not in self.player_dict:
                entity = Entity()
                self.player_dict[joystick] = entity
                self.entities.append(entity)
                position = Position(110, 110 + self.offset, 8)
                entity.add(position)
                entity.add(Movement())
                entity.add(Collision(10))
                entity.add(Friction(.95))
                entity.add(Image("assets/ball.gif", position))
                self.offset += 2
                # self.player_dict[joystick] = self.ball.get_rect()
        return self.player_dict

    @property
    def joysticks(self):
        if pygame.joystick.get_count() == len(self.joystick_list):
            return self.joystick_list
        self.joystick_list = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())][:8]
        for stick in self.joystick_list:
            stick.init()
        return self.joystick_list

    def get_movement(self, joystick):
        right_thumbstick_x = normalize_axis(joystick.get_axis(2))
        right_thumbstick_y = normalize_axis(joystick.get_axis(3))
        if right_thumbstick_x or right_thumbstick_y:
            self.moved = True
        return [right_thumbstick_x, right_thumbstick_y]

    def move_object(self, entity, movement):
        target = entity.get(Movement)
        target.vx += movement[0] / 100.0
        target.vy += movement[1] / 100.0

    def render(self):
        self.screen.fill(NOT_QUITE_BLACK)
        for entity in self.entities:
            image = entity.get(Image)
            if image:
                image.blit(self.screen)
            else:
                position = entity.get(Position)
                pygame.draw.circle(self.screen, RED, (floor(position.x), floor(position.y)), floor(position.radius), 1)

        pygame.display.flip()

    def main_loop(self):
        while True:
            milliseconds = self.clock.tick(FPS)
            self.playtime += milliseconds / 1000.0
            if self.playtime > 30 and not self.moved:
                # Probably a problem that locked us in full screen.
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                break
            for joystick in self.players.keys():
                self.move_object(self.players[joystick], self.get_movement(joystick))

            update_movement(self.entities)
            update_friction(self.entities)
            update_collisions(self.entities)
            update_boundary(self.entities)
            self.render()
