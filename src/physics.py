from math import sqrt
from .entity import entities_with


class Position:
    def __init__(self, x, y, radius):
        self.x = float(x)
        self.y = float(y)
        self.radius = float(radius)


class Movement:
    def __init__(self):
        self.vx = 0.0
        self.vy = 0.0


class Collision:
    def __init__(self, mass):
        self.mass = float(mass)


def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return sqrt(dx * dx + dy * dy)


def entity_overlap(entity_a, entity_b):
    a = entity_a.expect(Position)
    b = entity_b.expect(Position)
    cdistance = distance(a.x, a.y, b.x, b.y)
    return a.radius + b.radius - cdistance


def update_movement(entities):
    for entity in entities_with(entities, Movement):
        movement = entity.get(Movement)
        position = entity.get(Position)

        position.x += movement.vx
        position.y += movement.vy


def update_collisions(entities):
    active = entities_with(entities, Position)
    active = entities_with(active, Collision)
    active = list(entities_with(active, Movement))
    for entity in active:
        for other in active:
            if other == entity:
                continue
            overlap = entity_overlap(entity, other)
            if overlap > 0:
                movement = entity.get(Movement)
                mass = entity.get(Collision).mass
                position_a = entity.get(Position)
                position_b = entity.get(Position)

                movement.vx += abs(position_a.x - position_b.x) / mass * 10.0
                movement.vy += abs(position_b.y - position_b.y) / mass * 10.0


def random_entity():
    from random import random
    from entity import Entity
    # result = Entity(random() * 5 + 10, random() * 9 + 1)
    # result.x = random() * 10
    # result.y = random() * 10
    result = Entity()
    entity.add(Position(random() * 10, random() * 10))
    return result


### testing ###
if __name__ == '__main__':
    assert distance(0, 0, 0, 0) == 0
    assert distance(0, 0, 1, 0) == 1
    assert distance(-1, 0, 0, 0) == 1

    entities = []
    for _ in range(10):
        entities.append(random_entity())

    print(entities)
    for _ in range(3):
        update(entities)
        print(entities)
