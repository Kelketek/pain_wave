from math import floor

import pygame

from .physics import Position
from .facing import Facing

RED = 255, 0, 0
GREEN = 0, 255, 0
NOT_QUITE_BLACK = 22, 22, 22


class Image:
    def __init__(self, path, entity):
        position = entity.get(Position)
        self.image = pygame.transform.scale(
            pygame.image.load(path),
            (floor(position.radius * 2), floor(position.radius * 2))
        )
        self.entity = entity

    def blit(self, screen):
        position = self.entity.get(Position)
        if not position:
            # Removed from screen.
            pass
        rect = position_rect(position)
        screen.blit(self.image, rect)


def update_screen(entities, screen):
    screen.fill(NOT_QUITE_BLACK)
    for entity in entities:
        image = entity.get(Image)
        position = entity.get(Position)
        if image:
            image.blit(screen)
        else:
            pygame.draw.circle(screen, RED, (floor(position.x), floor(position.y)), floor(position.radius), 1)
        facing = entity.get(Facing)
        if facing and position:
            if facing.last_degrees != facing.degrees:
                radius, surface = direction_arrow(entity, facing.degrees)
                screen.blit(surface, position_rect(position, radius))

    pygame.display.flip()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def position_rect(position, radius=None):
    if radius is None:
        radius = position.radius
    return (
        floor(position.x - radius),
        floor(position.y - radius),
        floor(position.x + radius),
        floor(position.y - radius)
    )


def direction_arrow(entity, degrees):
    position = entity.get(Position)
    if not position:
        # Off the map.
        return
    radius = floor(position.radius * 2)
    if radius < 6:
        radius = 6
    top = (radius, 0)
    bottom_left = (radius - 3, (radius / 3))
    bottom_right = (radius + 3, (radius / 3))

    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32).convert_alpha()
    pygame.draw.polygon(surface, GREEN, (top, bottom_left, bottom_right))
    return radius, rot_center(surface, degrees)
