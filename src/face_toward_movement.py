from .entity import entities_with
from .facing import Facing
from .physics import Movement, degrees_from_point


class FaceTowardMovement:
    pass


def update_face_toward_movement(entities):
    for entity in entities_with(entities, FaceTowardMovement):
        facing = entity.get(Facing)
        movement = entity.get(Movement)
        if (not facing) or (not movement):
            continue
        # facing =
        angle = degrees_from_point(movement.vx, movement.vy)
        facing.degrees = angle
