import random
import time

import pygame

from game import Game
from maker import Maker
from unit import Unit

pygame.init()

screen = pygame.display.set_mode(
    # size=(640, 480),
    # size=(1280, 720),
    size=(1366, 768),
    # size=(1920, 1080),
    # flags=pygame.FULLSCREEN,
)

maker = Maker(screen)

game = Game(screen)

# unit = game.AddUnit(Unit(screen))
# unit.position = screen.get_rect().center

for i in range(int(screen.get_width() / 300)):
    game.AddRandomUnit()

game.AddGravity(screen.get_rect().center, random.randint(50, 100))
for i in range(random.randint(4, int(screen.get_width()/100))):
    game.AddGravity(
        (
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height())
        ),
        random.randint(10, 25),
    )

clock = pygame.time.Clock()

active = game

while True:
    for event in pygame.event.get():
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

    clock.tick(120)
    pygame.display.flip()
