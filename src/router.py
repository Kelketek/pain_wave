from src.grapple import Drag
from .entity import entities_with, Entity
from .friction import Friction
from .physics import entity_overlap, Movement, distance, degrees_from_point, rotate, Collision
from .facing import Facing
from .video import Image


router_counter = [1]


class Router:
    pass


class Routable:
    pass


def update_routers(entities):
    for entity in entities_with(entities, Router):
        for other in entities_with(entities, Routable):
            if entity_overlap(entity, other) > -20:
                facing = entity.get(Facing)
                movement = other.get(Movement)
                if not (facing and movement):
                    continue
                magnitude = distance(0, 0, movement.vx, movement.vy)
                result = rotate((0, 0), (0, magnitude), -facing.degrees)
                movement.vx, movement.vy = result

    # Towing sets facing
    for entity in entities_with(entities, Drag):
        drag = entity.get(Drag)
        if not drag.target.get(Router):
            continue
        facing = drag.target.expect(Facing)
        drag_facing = entity.expect(Facing)
        facing.degrees = drag_facing.degrees


def build_router():
    router_counter[0] += 1
    entity = Entity(name='Router {}'.format(router_counter[0]))
    entity.add(Movement())
    # entity.add(Facing(random.randint(0, 360), entity))
    entity.add(Facing(0, entity))
    entity.add(Collision(25))
    entity.add(Friction(.9))
    entity.add(Router())
    entity.add(Image('assets/router.png', entity))
    return entity
