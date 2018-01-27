# PLAY US A GAME! :V
from random import random
import pygame
import sys

from src.entity import Entity
from src.hardware import Controller, update_input
from src.logic import Timer, update_triggers, update_timers
from src.physics import Position, Movement, update_movement, update_collisions, Collision
from src.boundary import update_boundary
from src.friction import update_friction, Friction
from src.grapple import update_grapple, CanGrapple


# Desired framerate in frames per second. Try out other values.
from src.video import Image, update_screen
from src.violence import Transmitter

FPS = 30

BLACK = 0, 0, 0


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
        self.entities = []

        for _ in range(10):
            entity = Entity()
            self.entities.append(entity)
            entity.add(Position(random() * 250, random() * 250, random() * 12 + 8))
            entity.add(Movement())
            entity.add(Collision(random() * 10 + 40))
            entity.add(Friction(.9))

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
            entity.add(Friction(.95))
            entity.add(Image("assets/ball.gif", position))
            entity.add(Controller(joystick))
            entity.add(CanGrapple())
            self.offset += 2

    def init_environment(self):
        cannon = Entity(name='Death Wave Transmitter')
        position = Position(0, self.height / 2, 5)
        cannon.add(position)
        emitter = Transmitter(position)
        cannon.add(emitter)
        cannon.add(Timer(5, self.playtime, tasks=[emitter.create_projectile]))
        self.entities.append(cannon)

    def main_loop(self):
        while True:
            milliseconds = self.clock.tick(FPS)
            self.playtime += milliseconds / 1000.0
            if self.playtime > 180 and not self.moved:
                # Probably a problem that locked us in full screen.
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # if event.type == pygame.JOYBUTTONDOWN:
                #     print(repr(event.button))

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                break

            update_triggers(self.entities)
            update_timers(self.entities, self.playtime)
            update_input(self.entities)
            update_movement(self.entities)
            update_boundary(self.entities)
            update_friction(self.entities)
            update_collisions(self.entities)
            update_grapple(self.entities)
            update_screen(self.entities, self.screen)
