from random import random

from src.entity import Entity
from src.friction import Friction
from src.hardware import Controller
from src.physics import Collision, Movement, Position
from src.violence import PlayerState, Vulnerable


class Dispenser:
    def __init__(self, team, entity):
        self.hopper = []
        self.team = team
        self.entity = entity

    def dispense(self, entities):
        for entity in entities[:]:
            state = entity.get(PlayerState)
            vulnerable = entity.get(Vulnerable)
            if state and state.team == self.team and vulnerable.dead:
                self.hopper.append(entity)
                entities.remove(entity)
                entity.dead = False
                entity.remove_type(Position)
        while len(self.hopper) < 5:
            self.hopper.insert(0, build_wall(place=False))
        self.drop(entities)

    def drop(self, entities):
        loot = self.hopper.pop()
        position = self.entity.get(Position)
        controller = loot.get(Controller)
        if controller:
            controller.disabled = False
        vulnerable = loot.get(Vulnerable)
        if vulnerable:
            vulnerable.dead = False
        movement = loot.get(Movement)
        movement.vy = -1
        loot.add(Position(position.x, position.y, rand_radius()))
        entities.append(loot)


def rand_radius():
    return random() * 12 + 8


def build_wall(place=True):
    entity = Entity()
    if place:
        entity.add(Position(random() * 250, random() * 250, rand_radius()))
    entity.add(Movement())
    entity.add(Collision(random() * 10 + 40))
    entity.add(Friction(.9))
    return entity
