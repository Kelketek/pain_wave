# PLAY US A GAME! :V
import pygame
import sys

pygame.init()
pygame.mixer.init()

from .support import Dispenser
from .entity import Entity, entities_with
from .hardware import Controller, update_input
from .logic import Timer, update_triggers, update_timers, Restart, Quit
from .physics import Position, Movement, update_movement, update_collisions, Collision
from .boundary import update_boundary
from .friction import update_friction, Friction
from .grapple import update_grapple, CanGrapple
from .video import Image, update_screen
from .violence import Transmitter, Team, Vulnerable
from .router import update_routers
from .game_over import EndGameplayOnDeath, update_end_gameplay
from .facing import Facing
from .face_toward_movement import update_face_toward_movement


# Desired framerate in frames per second. Try out other values.
FPS = 30

FIRE_INTERVAL = 6

DISPENSE_INTERVAL = FIRE_INTERVAL * 3


class PainWave:
    def __init__(self, width=1200, height=1200):
        self.size = self.width, self.height = width, height
        self.background = pygame.image.load("assets/background.png")
        self.playtime = 0.0
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.HWACCEL)
        self.clock = pygame.time.Clock()
        pygame.init()
        pygame.joystick.init()
        pygame.mouse.set_visible(0)
        self.entities = []
        self.init_environment()
        self.loser = None

    def restart(self):
        self.entities = []
        self.init_environment()
        self.loser = None
        pygame.mixer.music.load('assets/Background Music 18sec. Loop.wav')
        pygame.mixer.music.play(-1)

    def init_players(self):
        for i, joystick in enumerate(range(pygame.joystick.get_count())):
            team = (i % 2) + 1
            joystick = pygame.joystick.Joystick(joystick)
            joystick.init()
            entity = Entity(name='Player {}'.format(i))
            self.entities.append(entity)
            position = Position(*self.dispenser_position(team), radius=12)
            entity.add(position)
            entity.add(Movement())
            entity.add(Collision(10))
            entity.add(Friction(.95))
            entity.add(Image('assets/character.png', entity, fixed_rotation=True))
            entity.add(Controller(joystick))
            entity.add(CanGrapple())
            entity.add(Team(team=team))
            entity.add(Vulnerable(
                tombstone=True,
                next_image=Image('assets/character_dead.png', entity, fixed_rotation=True)
            ))
            entity.add(Facing(0, entity))

    def make_cannon(self, x, y, velocity, offset, angle, team):
        cannon = Entity(name='Pain Wave Transmitter')
        position = Position(x, y, 5)
        cannon.add(position)
        transmitter = Transmitter(position, velocity=velocity, offset=offset)
        cannon.add(transmitter)
        cannon.add(Timer(FIRE_INTERVAL, self.playtime, tasks=[transmitter.create_projectile]))
        cannon.add(EndGameplayOnDeath())
        cannon.add(Vulnerable(tombstone=True))
        cannon.add(Collision(100))
        cannon.add(Team(team=team))
        cannon.add(Image('assets/transmitter.png', cannon))
        cannon.add(Facing(angle, cannon))
        self.entities.append(cannon)

    def dispenser_position(self, team):
        offset = 50
        if team == 1:
            return (offset / 2), (self.height / 2)
        else:
            return (self.width - (offset / 2)), (self.height / 2)

    def make_dispenser(self, x, y, team):
        tetris_god = Entity(name='Dispensor for team {}'.format(team + 1))
        dispenser = Dispenser(team=team, entity=tetris_god)
        tetris_god.add(dispenser)
        tetris_god.add(Position(x, y, 18))
        tetris_god.add(Timer(DISPENSE_INTERVAL, self.playtime, tasks=[dispenser.dispense]))
        tetris_god.add(Image('assets/dispenser.png', tetris_god))
        self.entities.append(tetris_god)
        dispenser.dispense(self.entities)

    def init_environment(self):
        offset = 100
        self.make_cannon(0 + offset, self.height / 2, (4, 0), (18, 0), angle=90, team=1)
        self.make_cannon(self.width - offset, self.height / 2, (-4, 0), (-18, 0), angle=-90, team=2)
        self.make_dispenser(*self.dispenser_position(1), team=1)
        self.make_dispenser(*self.dispenser_position(2), team=2)
        self.init_players()

    @property
    def winner(self):
        if self.loser:
            return 1 if self.loser == 2 else 2
        else:
            return None

    def main_loop(self):
        import pygame

        pygame.mixer.music.load('assets/Background Music 18sec. Loop.wav')
        pygame.mixer.music.play(-1)

        while True:
            milliseconds = self.clock.tick(FPS)
            self.playtime += milliseconds / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                break

            if not self.loser:
                self.loser = update_end_gameplay(self.entities)
            update_triggers(self.entities)
            update_timers(self.entities, self.playtime)
            update_input(self.entities)
            update_movement(self.entities)
            update_routers(self.entities)
            update_boundary(self.entities)
            update_friction(self.entities)
            update_collisions(self.entities)
            update_grapple(self.entities)
            update_face_toward_movement(self.entities)
            # must update screen last to avoid visual latency
            update_screen(self.entities, self.screen, self.background, winner=self.winner)
            if list(entities_with(self.entities, Quit)):
                break
            if list(entities_with(self.entities, Restart)):
                self.restart()
