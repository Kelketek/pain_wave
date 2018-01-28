from math import floor

import pygame

from .physics import Position, rotate
from .facing import Facing

RED = 255, 0, 0
GREEN = 0, 255, 0
BACKGROUND = 22, 22, 22


class Image:
    def __init__(self, path, entity):
        self.path = path
        self.image = None
        self.entity = entity
        self.cached = None
        self.last_degrees = None

    def blit(self, screen, degrees=None):
        position = self.entity.get(Position)
        if not position:
            # Removed from screen.
            return
        if not self.image:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(self.path),
                (floor(position.radius * 2), floor(position.radius * 2))
            )
        if not (self.cached and self.last_degrees == degrees):
            if degrees is not None:
                self.cached = rot_center(self.image, degrees + 180)
            else:
                self.cached = self.image
            self.last_degrees = degrees
        rect = position_rect(position)
        screen.blit(self.cached, rect)


def update_screen(entities, screen, background, winner=None):
    screen.blit(background, ((0, 0), (screen.get_width(), screen.get_height())))
    for entity in entities:
        image = entity.get(Image)
        position = entity.get(Position)
        facing = entity.get(Facing)
        degrees = (facing or 0) and facing.degrees
        if image:
            image.blit(screen, degrees)
        else:
            pygame.draw.circle(screen, RED, (floor(position.x), floor(position.y)), floor(position.radius), 1)
        if facing and position:
            if facing.last_degrees != facing.degrees:
                radius, surface = direction_arrow(entity, facing.degrees)
                screen.blit(surface, position_rect(position, radius))

    if winner:
        declare_winner(screen, winner)

    pygame.display.flip()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotozoom(image, angle, 1)
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
    return radius, rot_center(surface, degrees + 180)


def declare_winner(screen, winner):
    basicfont = pygame.font.SysFont(None, 120)
    text = basicfont.render('Team {} Wins!'.format(winner), True, (255, 0, 0), None)
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery

    screen.blit(text, textrect)
