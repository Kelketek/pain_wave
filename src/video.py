from math import floor

import pygame

from src.physics import Position

RED = 255, 0, 0
NOT_QUITE_BLACK = 22, 22, 22


class Image:
    def __init__(self, path, position, depth=0):
        self.image = pygame.transform.scale(
            pygame.image.load(path),
            (floor(position.radius * 2), floor(position.radius * 2))
        )
        self.position = position

    def blit(self, screen):
        rect = (
            floor(self.position.x - self.position.radius),
            floor(self.position.y - self.position.radius),
            floor(self.position.x + self.position.radius),
            floor(self.position.y - self.position.radius)
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