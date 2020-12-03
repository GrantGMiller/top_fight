import random
import time

import pygame

from game import Game
from maker import Maker
from unit import Unit

pygame.init()

screen = pygame.display.set_mode(
    size=(640, 480),
)

maker = Maker(screen)

game = Game(screen)
unit = game.AddUnit(Unit(screen))
unit._position = screen.get_rect().center
unit.velocity = (200, 200)
unit.angularVelocity = 100

# for i in range(random.randint(1, 10)):
#     game.AddGravity(
#         (
#             random.randint(0, screen.get_width()),
#             random.randint(0, screen.get_height())
#         ),
#         random.randint(5, 25),
#     )

clock = pygame.time.Clock()
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        maker.Event(event)

    game.Draw(clock)

    # OSD #######################
    fps = int(clock.get_fps())

    degPerSec = game.units[0].angularVelocity
    degPerMin = degPerSec * 60
    revPerMin = int(degPerMin / 360)

    font = pygame.font.Font(None, 24)
    surface_osd = font.render(
        f'FPS: {fps}, RPM: {revPerMin}, Pos: {game.units[0].center}, Acc: {int(game.units[0].acceleration[0])}, {int(game.units[0].acceleration[1])}, Vel: {int(game.units[0].velocity[0])}, {int(game.units[0].velocity[1])}',
        True,
        pygame.color.Color('white') if fps > 45 else pygame.color.Color('red'),

    )
    screen.blit(surface_osd, (0, 0))

    clock.tick(120)
    pygame.display.flip()
