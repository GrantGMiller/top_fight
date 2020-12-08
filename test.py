import random
import sys
import time

import pygame

from boosters import SpinBooster
from choose_top import Choose
from game import Game
from maker import Maker
from unit import Unit
from winner import Winner

pygame.init()

screen = pygame.display.set_mode(
    # size=(640, 480),
    # size=(1280, 720),
    size=(1366, 768),
    # size=(1920, 1080),
    # flags=pygame.FULLSCREEN,
)

game = Game(screen)

unit = game.AddUnit(
    Unit(
        screen,
    )
)
fromLeft = True

unit.position = (
    screen.get_width() / 2 - 150 if fromLeft else screen.get_width() / 2 + 150,
    unit.height / 2
)
unit.velocity = (25 if fromLeft else -25, 0)
unit.angularVelocity = 0

game.AddBooster(
    SpinBooster(
        pos=(
            int(screen.get_width() / 2),
            int(unit.position[1])
        ),
        game=game,
    )
)

clock = pygame.time.Clock()
active = game

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        active.Event(event)

    active.Draw(clock)
    # OSD #######################
    fps = int(clock.get_fps())

    font = pygame.font.Font(None, 24)
    surface_osd = font.render(
        f'FPS: {fps}',
        True,
        pygame.color.Color('white') if fps > 45 else pygame.color.Color('red'),

    )
    screen.blit(surface_osd, (0, 0))

    clock.tick()
    pygame.display.flip()
