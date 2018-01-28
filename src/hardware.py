from math import floor

from src.entity import entities_with
from src.logic import Restart, Quit
from .physics import Movement, degrees_from_point
from .facing import Facing

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
    value *= 200
    value /= 15
    return floor(value)


class Controller:
    def __init__(self, joystick):
        self.joystick = joystick
        self.moved = False
        self.disabled = False
        self.menu = False


def move_object(entity, movement):
    target = entity.get(Movement)
    target.vx += movement[0] / 100.0
    target.vy += movement[1] / 100.0


def get_movement(controller):
    left_thumbstick_x = normalize_axis(controller.joystick.get_axis(0))
    right_thumbstick_y = normalize_axis(controller.joystick.get_axis(1))
    return [left_thumbstick_x, right_thumbstick_y]


def update_input(entities):
    for entity in entities_with(entities, Controller):
        controller = entity.get(Controller)
        if not (controller.disabled or controller.menu):
            movement = get_movement(controller)
            if movement[0] or movement[1]:
                move_object(entity, get_movement(controller))
                facing = entity.get(Facing)
                facing.degrees = degrees_from_point(*movement)
        elif controller.menu:
            if controller.joystick.get_button(12):
                # Restart the game
                entity.add(Restart())
            if controller.joystick.get_button(14):
                # Quit the game.
                entity.add(Quit())
