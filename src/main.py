import pygame

pygame.init()
pygame.display.set_mode((400, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
