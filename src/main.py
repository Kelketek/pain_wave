# PLAY US A GAME! :V
from math import floor

import pygame
import sys


def get_joysticks():
    return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


def normalize_axis(value):
    if 0 < value < .05:
        value = 0
    if .05 > value > 0:
        value = 0
    if value:
        if value > 0:
            value -= .05
        else:
            value += .05
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


class PainWave:
    def __init__(self, width=600, height=600):
        pygame.init()
        pygame.joystick.init()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(0)
        self.size = self.width, self.height = width, height
        self.playtime = 0.0
        self.moved = False

        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWACCEL)
        self.ball = pygame.image.load("assets/ball.gif")
        self.ball_rect = self.ball.get_rect()
        pygame.joystick.init()
        self.joystick_list = []
        self.player_dict = {}

    @property
    def players(self):
        if len(self.player_dict) == len(self.joysticks):
            return self.player_dict
        for joystick in self.joysticks:
            if joystick not in self.player_dict:
                self.player_dict[joystick] = self.ball.get_rect()
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
        return [right_thumbstick_x, right_thumbstick_y]

    def move_object(self, obj_rect, movement):
        obj_rect = obj_rect.move(movement)
        if obj_rect.left < 0:
            obj_rect = obj_rect.move([-obj_rect.left, 0])
        if obj_rect.right > self.width:
            obj_rect = obj_rect.move([(self.width - obj_rect.right), 0])
        if obj_rect.top < 0:
            obj_rect = obj_rect.move([0, -obj_rect.top])
        if obj_rect.bottom > self.height:
            obj_rect = obj_rect.move([0, (self.height - obj_rect.bottom)])
        return obj_rect

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

            self.screen.fill(BLACK)
            for joystick in self.players.keys():
                self.players[joystick] = self.move_object(self.players[joystick], self.get_movement(joystick))
                self.screen.blit(self.ball, self.players[joystick])

            text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)
            pygame.display.flip()
