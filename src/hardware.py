from math import floor

from src.physics import Movement

DEAD_ZONE = .1


def normalize_axis(value):
    if 0 < value < DEAD_ZONE:
        value = 0
    if DEAD_ZONE > value > 0:
        value = 0
    if value:
        if value > 0:
            value -= DEAD_ZONE
        else:
            value += DEAD_ZONE
    value *= 100
    value /= 15
    return floor(value)


class Controller:
    def __init__(self, joystick):
        self.joystick = joystick
        self.moved = False


def move_object(entity, movement):
    target = entity.get(Movement)
    target.vx += movement[0] / 100.0
    target.vy += movement[1] / 100.0


def get_movement(controller):
    right_thumbstick_x = normalize_axis(controller.joystick.get_axis(2))
    right_thumbstick_y = normalize_axis(controller.joystick.get_axis(3))
    return [right_thumbstick_x, right_thumbstick_y]


def update_input(entities):
    for entity in entities:
        controller = entity.get(Controller)
        if controller:
            move_object(entity, get_movement(controller))
