from math import sqrt, floor, atan2, pi, cos, sin

import math

from .entity import entities_with


class Position:
    def __init__(self, x, y, radius):
        self.x = float(x)
        self.y = float(y)
        self.radius = float(radius)


class Movement:
    def __init__(self, vx=0.0, vy=0.0):
        self.vx = vx
        self.vy = vy


class Collision:
    def __init__(self, mass):
        self.mass = float(mass)


# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
def rotate(origin, point, degrees):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    ox, oy = origin
    px, py = point
    angle = math.radians(degrees)

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy


def degrees_from_point(x, y):
    """Assuming a first point of 0, 0 calculates the degree of an angle
    """
    return atan2(x, y) * floor(180 / pi)


def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return sqrt(dx * dx + dy * dy)


def entity_distance(entity_a, entity_b):
    a = entity_a.expect(Position)
    b = entity_b.expect(Position)
    return distance(a.x, a.y, b.x, b.y)


def entity_gap(entity_a, entity_b):
    a = entity_a.expect(Position)
    b = entity_b.expect(Position)
    return distance(a.x, a.y, b.x, b.y) - a.radius - b.radius


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
    passive = entities_with(entities, Position)
    passive = list(entities_with(passive, Collision))
    active = list(entities_with(passive, Movement))
    for entity in active:
        for other in passive:
            if other == entity:
                continue
            overlap = entity_overlap(entity, other)
            if overlap > 0:
                movement = entity.get(Movement)
                mass = entity.get(Collision).mass
                position_a = entity.get(Position)
                position_b = other.get(Position)

                movement.vx += (position_a.x - position_b.x) / mass / 8.0
                movement.vy += (position_a.y - position_b.y) / mass / 8.0
