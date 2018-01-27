from .entity import entities_with
from .physics import distance, Movement, Position, Collision


class Grapple:
    def __init__(self, target):
        self.target = target


def update_grapple(entities):
    for entity in entities_with(entities, Grapple):
        grapple = entity.get(Grapple)
        position_a = entity.expect(Position)
        position_b = grapple.target.expect(Position)
        cdistance = distance(position_a.x, position_a.y, position_b.x, position_b.y)
        both_radii = position_a.radius + position_b.radius
        if cdistance > both_radii * 1.05:
            movement_a = entity.get(Movement)
            mass_a = entity.get(Collision).mass
            movement_a.vx += -(position_a.x - position_b.x) / mass_a / 20.0
            movement_a.vy += -(position_a.y - position_b.y) / mass_a / 20.0

            movement_b = grapple.target.get(Movement)
            mass_b = grapple.target.get(Collision).mass
            movement_b.vx += (position_a.x - position_b.x) / mass_b / 6.0
            movement_b.vy += (position_a.y - position_b.y) / mass_b / 6.0
