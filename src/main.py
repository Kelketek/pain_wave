# PLAY US A GAME! :V

import pygame
import sys


def get_joysticks():
    return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


DIRECT_MAP = {
    pygame.K_w: (0, -3),
    pygame.K_a: (-3, 0),
    pygame.K_s: (0, 3),
    pygame.K_d: (3, 0)
}


def main():
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)
    size = width, height = 600, 600
    black = 0, 0, 0
    playtime = 0.0

    # Desired framerate in frames per second. Try out other values.
    FPS = 30

    screen = pygame.display.set_mode(size)
    ball = pygame.image.load("assets/ball.gif")
    ballrect = ball.get_rect()

    while True:

        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        movement = [0, 0]

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            break

        for key, value in DIRECT_MAP.items():
            if pressed[key]:
                movement = [movement[0] + DIRECT_MAP[key][0], movement[1] + DIRECT_MAP[key][1]]

        ballrect = ballrect.move(movement)
        if ballrect.left < 0:
            ballrect = ballrect.move([-ballrect.left, 0])
        if ballrect.right > width:
            ballrect = ballrect.move([(width - ballrect.right), 0])
        if ballrect.top < 0:
            ballrect = ballrect.move([0, -ballrect.top])
        if ballrect.bottom > height:
            ballrect = ballrect.move([0, (height - ballrect.bottom)])

        screen.fill(black)
        screen.blit(ball, ballrect)
        text = "FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(), playtime)
        pygame.display.set_caption(text)
        pygame.display.flip()
