from .entity import entities_with
from .physics import entity_overlap, Movement


class Router:
    pass


class Routable:
    pass


def update_routers(entities):
    for entity in entities_with(entities, Router):
        for other in entities_with(entities, Routable):
            if entity_overlap(entity, other) > 0:
                # TODO: Need facing module
                movement = other.get(Movement)
                movement.vx = 2
                movement.vy = 2
