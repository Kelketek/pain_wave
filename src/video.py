from math import floor

import pygame

from src.physics import Position

RED = 255, 0, 0
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
        rect = (
            floor(position.x - position.radius),
            floor(position.y - position.radius),
            floor(position.x + position.radius),
            floor(position.y - position.radius)
        )
        screen.blit(self.image, rect)


def update_screen(entities, screen):
    screen.fill(NOT_QUITE_BLACK)
    for entity in entities:
        image = entity.get(Image)
        if image:
            image.blit(screen)
        else:
            position = entity.get(Position)
            pygame.draw.circle(screen, RED, (floor(position.x), floor(position.y)), floor(position.radius), 1)

    pygame.display.flip()
