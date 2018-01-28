from .entity import entities_with
from .physics import Movement, Position

FIELD_WIDTH = 1200
FIELD_HEIGHT = 1200

def update_boundary(entities):
    for entity in entities_with(entities, Movement):
        position = entity.get(Position)
        if position is None:
            continue
        movement = entity.get(Movement)
        if position.x < position.radius:
            position.x = position.radius
            if movement.vx < 0:
                movement.vx = -movement.vx
        if position.y < position.radius:
            position.y = position.radius
            if movement.vy < 0:
                movement.vy = -movement.vy
        if position.x > FIELD_WIDTH - position.radius:
            position.x = FIELD_WIDTH - position.radius
            if movement.vx > 0:
                movement.vx = -movement.vx
        if position.y > FIELD_HEIGHT - position.radius:
            position.y = FIELD_HEIGHT - position.radius
            if movement.vy > 0:
                movement.vy = -movement.vy
