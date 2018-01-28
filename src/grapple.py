import pygame

from .hardware import Controller
from .entity import entities_with
from .physics import distance, Movement, Position, Collision, entity_distance, entity_gap


grab_sound = pygame.mixer.Sound('assets/grapple.ogg')


class CanGrapple:
    def __init__(self):
        pass


class Drag:
    def __init__(self, target):
        self.target = target


def nearest_to(entities, subject):
    result = None
    result_distance = None
    for other in entities:
        if other == subject:
            continue
        elif not result:
            result = other
            result_distance = entity_distance(subject, other)
        else:
            cdistance = entity_distance(subject, other)
            if cdistance < result_distance:
                result = other
                result_distance = cdistance
    return result


def update_grapple(entities):
    # Grapple controls
    for entity in entities_with(entities, CanGrapple):
        controller = entity.get(Controller)
        if controller is None:
            continue
        if controller.joystick.get_button(11):
            if entity.get(Drag) is None:
                dragables = entities_with(entities, Collision)
                dragables = entities_with(dragables, Movement)
                nearest = nearest_to(dragables, entity)
                if nearest and entity_gap(entity, nearest) < 1:
                    entity.add(Drag(nearest))
                    grab_sound.play()
        elif entity.get(Drag):
            entity.remove_type(Drag)
            grab_sound.play()

    # Dragging
    for entity in entities_with(entities, Drag):
        drag = entity.get(Drag)
        position_a = entity.expect(Position)
        position_b = drag.target.expect(Position)
        cdistance = distance(position_a.x, position_a.y, position_b.x, position_b.y)
        both_radii = position_a.radius + position_b.radius
        if cdistance > both_radii * 1.05:
            movement_a = entity.get(Movement)
            collision_a = entity.get(Collision)
            if collision_a:
                mass_a = collision_a.mass
                movement_a.vx += -(position_a.x - position_b.x) / mass_a / 20.0
                movement_a.vy += -(position_a.y - position_b.y) / mass_a / 20.0

            movement_b = drag.target.get(Movement)
            if movement_b:
                collision = drag.target.get(Collision)
                if not collision:
                    # Mass was removed in previously processed event.
                    continue
                mass_b = drag.target.get(Collision).mass
                movement_b.vx += (position_a.x - position_b.x) / mass_b / 6.0
                movement_b.vy += (position_a.y - position_b.y) / mass_b / 6.0
