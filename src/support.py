from random import random

from .entity import Entity
from .friction import Friction
from .hardware import Controller
from .physics import Collision, Movement, Position
from .router import build_router, Router
from .video import Image
from .violence import Team, Vulnerable
from .logic import Timer


wall_counter = [0]


class Dispenser:
    def __init__(self, team, entity):
        self.hopper = []
        self.team = team
        self.entity = entity

    def dispense(self, entities):
        for entity in entities[:]:
            state = entity.get(Team)
            vulnerable = entity.get(Vulnerable)
            if state and state.team == self.team and vulnerable.dead:
                self.hopper.append(entity)
                entities.remove(entity)
                vulnerable.dead = False
        while len(self.hopper) < 5:
            if random() < .25:
                self.hopper.insert(0, build_router())
            else:
                self.hopper.insert(0, build_wall())
        self.drop(entities)

    def drop(self, entities):
        loot = self.hopper.pop()
        loot.remove_type(Timer)
        position = self.entity.get(Position)
        controller = loot.get(Controller)
        router = loot.get(Router)
        if controller:
            controller.disabled = False
            # Is a player.
            loot.replace(Image('assets/character.png', loot, fixed_rotation=True))
            radius = loot.get(Position).radius
            loot.replace(Position(position.x, position.y, radius))
            loot.add(Collision(10))
        elif router:
            loot.add(Position(position.x, position.y, 20))
        else:
            loot.add(Position(position.x, position.y, rand_radius()))
        vulnerable = loot.get(Vulnerable)
        if vulnerable:
            vulnerable.dead = False
        movement = loot.get(Movement)
        movement.vy = -.2
        entities.append(loot)


def rand_radius():
    return random() * 24 + 16


def build_wall():
    wall_counter[0] += 1
    entity = Entity(name='Wall {}'.format(wall_counter[0]))
    entity.add(Movement())
    entity.add(Collision(random() * 10 + 40))
    entity.add(Friction(.9))
    entity.add(Image('assets/wall.png', entity))
    return entity
