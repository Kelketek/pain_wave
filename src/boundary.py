from .entity import entities_with
from .physics import Movement, Position


FIELD_WIDTH = 600
FIELD_HEIGHT = 600


class DieOnReflect:
    pass


def update_boundary(entities):
    for entity in entities_with(entities, Movement):
        position = entity.get(Position)
        if position is None:
            continue
        reflected = False
        movement = entity.get(Movement)
        if position.x < position.radius:
            reflected = True
            position.x = position.radius
            if movement.vx < 0:
                movement.vx = -movement.vx
        if position.y < position.radius:
            reflected = True
            position.y = position.radius
            if movement.vy < 0:
                movement.vy = -movement.vy
        if position.x > FIELD_WIDTH - position.radius:
            reflected = True
            position.x = FIELD_WIDTH - position.radius
            if movement.vx > 0:
                movement.vx = -movement.vx
        if position.y > FIELD_HEIGHT - position.radius:
            reflected = True
            position.y = FIELD_HEIGHT - position.radius
            if movement.vy > 0:
                movement.vy = -movement.vy

        if reflected and entity.get(DieOnReflect):
            try:
                entities.remove(entity)
            except ValueError:
                pass
