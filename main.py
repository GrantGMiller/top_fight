import random
import sys
import time

import pygame

from choose_top import Choose
from game import Game
from maker import Maker
from winner import Winner

pygame.init()

pygame.display.set_caption('Dreidel Blades')


screen = pygame.display.set_mode(
    # size=(640, 480),
    # size=(1280, 720),
    size=(1366, 768),
    # size=(1920, 1080),
    # flags=pygame.FULLSCREEN,
)

maker = Maker(screen)

choose = Choose(screen)
clock = pygame.time.Clock()

active = choose

lastGameEndTime = None
gameOverTime = None
while True:

    if isinstance(active, Choose):
        if active.startGameWith is not None:
            index, stats = active.startGameWith
            game = Game(screen)
            game.NewGame(index, stats, numUnits=1, name='Player 1')
            gameOverTime = None
            active = game

    elif isinstance(active, Game):
        if game.gameOver:
            if gameOverTime is None:
                gameOverTime = time.time()
            if time.time() - gameOverTime > 5:
                active = Winner(game.units[0], screen)
                lastGameEndTime = time.time()

    elif isinstance(active, Winner) and time.time() - lastGameEndTime > 5:
        # game = Game(screen)
        # game.NewGame(numUnits=2)
        # gameOverTime = None
        # active = game

        active = Choose(screen)

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

    clock.tick(120)
    pygame.display.flip()
