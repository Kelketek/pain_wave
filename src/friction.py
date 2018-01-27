from .entity import entities_with
from .physics import Movement


class Friction:
    def __init__(self, factor):
        self.factor = float(factor)


def update_friction(entities):
    for entity in entities_with(entities, Friction):
        friction = entity.get(Friction)
        movement = entity.get(Movement)
        movement.vx *= friction.factor
        movement.vy *= friction.factor
