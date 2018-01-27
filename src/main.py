# PLAY US A GAME! :V
from math import floor
from random import random

import pygame
import sys

from src.entity import Entity
from src.hardware import Controller, update_input
from src.logic import Emitter, Timer, update_triggers, update_timers
from src.physics import Position, Movement, update_movement, update_collisions, Collision
from src.boundary import update_boundary
from src.friction import update_friction


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
        pygame.joystick.init()
        self.entities = []

        for _ in range(10):
            entity = Entity()
            self.entities.append(entity)
            entity.add(Position(random() * 250, random() * 250, random() * 12 + 8))
            entity.add(Movement())
            entity.add(Collision(random() * 10 + 40))

        self.init_players()
        self.init_environment()

    def init_players(self):
        for joystick in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(joystick)
            joystick.init()
            entity = Entity()
            self.entities.append(entity)
            position = Position(110, 110 + self.offset, 8)
            entity.add(position)
            entity.add(Movement())
            entity.add(Collision(10))
            entity.add(Image("assets/ball.gif", position))
            entity.add(Controller(joystick))
            self.offset += 2

    def init_environment(self):
        cannon = Entity(name='Death Wave Emitter')
        position = Position(0, self.height / 2, 5)
        cannon.add(position)
        emitter = Emitter(position)
        cannon.add(emitter)
        cannon.add(Timer(5, self.playtime, tasks=[emitter.create_projectile]))
        self.entities.append(cannon)

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

            update_triggers(self.entities)
            update_timers(self.entities, self.playtime)
            update_input(self.entities)
            update_movement(self.entities)
            update_friction(self.entities)
            update_collisions(self.entities)
            update_boundary(self.entities)
            self.render()
