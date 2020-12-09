import math
import os
import random
import time
from pathlib import Path
import helpers
import stats
from physics import Physics

import pygame

IMG_DIR = r'parts'
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

    for url in [
        'https://raw.githubusercontent.com/GrantGMiller/top_fight/master/parts/1.png',

    ]

COLOR_MAP = {
    'attack': pygame.color.Color((255, 127, 127)),
    'defense': pygame.color.Color((127, 255, 127)),
    'spin': pygame.color.Color((127, 127, 255))
}


class Choose:
    def __init__(self, screen):
        self.screen = screen
        self.physics = Physics(
            (0, 0, 1, 1),
            friction=5000,
        )
        self.imgSize = int(self.screen.get_width() / 4)
        self.images = [
            pygame.transform.scale(pygame.image.load(IMG_DIR + '/' + path), (self.imgSize, self.imgSize)) for path in
            os.listdir(IMG_DIR)
        ]
        # self.currentSelection = int(len(self.images) / 2)
        self.currentSelection = random.choice(list(range(len(self.images))))
        self.surfName = None

        self.stats = ['attack', 'defense', 'spin']
        self.statSurf = pygame.Surface((
            int(self.screen.get_width()),
            int((self.screen.get_height() - self.imgSize) / 2),
        ))

        self.startGameWith = None

        self.UpdateTextSurfaces()
        self.startTime = time.time()

    def UpdateTextSurfaces(self):
        self.surfName = pygame.font.Font(None, int(self.screen.get_height() / 10)).render(
            f'Current selection: {self.currentSelection}',
            True,
            pygame.color.Color('white')
        )

        yOffset = 0
        for stat in self.stats:
            surfStatTitle = pygame.font.Font(None, int(self.screen.get_height() / 10)).render(
                f'{stat}: ',
                True,
                pygame.color.Color('white')
            )
            surfBar = pygame.Surface((
                int(self.statSurf.get_width() / 10),
                int(self.statSurf.get_height() / len(self.stats))
            ))
            # fill the bar with grey
            pygame.draw.rect(
                surfBar,
                pygame.color.Color('grey'),
                (
                    0,
                    0,
                    surfBar.get_width(),
                    surfBar.get_height(),
                )
            )
            value = stats.GetStats(self.currentSelection)[stat]
            pygame.draw.rect(
                surfBar,
                COLOR_MAP.get(stat, helpers.GetRandomColor(stat)),
                (
                    0,
                    0,
                    (value / surfBar.get_width()) * surfBar.get_width(),
                    surfBar.get_height(),
                )
            )
            self.statSurf.blit(
                surfStatTitle,
                (
                    self.statSurf.get_rect().centerx - surfStatTitle.get_width(),
                    yOffset
                )
            )
            self.statSurf.blit(
                surfBar,
                (
                    self.statSurf.get_rect().centerx,
                    yOffset,
                )
            )

            yOffset += surfBar.get_height()

    def Event(self, event):
        print('event=', event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.currentSelection += 1
            elif event.key == pygame.K_LEFT:
                self.currentSelection -= 1

            self.currentSelection = min(len(self.images) - 1, self.currentSelection)
            self.currentSelection = max(0, self.currentSelection)

            self.UpdateTextSurfaces()

            self.startTime = time.time()

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
            self.startGameWith = (
                self.images[self.currentSelection],
                stats.GetStats(self.currentSelection)
            )
            print('startGameWith=', self.startGameWith)

    def Draw(self, clock):
        self.screen.fill((0, 0, 0))
        deltaTime = clock.get_time() / 1000

        xOffset = 0
        yOffset = (self.screen.get_height() - self.imgSize) / 2
        spacer = 100

        desiredX = 0

        for index, img in enumerate(self.images):
            self.screen.blit(
                img,
                (
                    xOffset + self.physics.x,
                    yOffset + self.physics.y
                ),
            )
            if index == self.currentSelection:
                desiredX = -xOffset + self.screen.get_width() / 2 - self.images[0].get_width() / 2

            xOffset += spacer + self.imgSize

        self.physics.ApplyPhysics(clock)
        delta = desiredX - self.physics.x

        if -self.imgSize / 10 < delta < self.imgSize / 10:
            self.physics.velocity *= 0.1

            if self.physics.velocity.magnitude() < 1:
                self.physics.velocity = (0, 0)
            self.physics.acceleration = (0, 0)
        else:
            self.physics.acceleration = (10000 if delta > 0 else -10000, 0)

        # draw text
        self.screen.blit(
            self.surfName,
            (
                (self.screen.get_width() - self.surfName.get_width()) / 2,
                int(self.screen.get_height() / 10)
            )
        )

        # stats
        self.screen.blit(
            self.statSurf,
            (
                0,
                int(self.screen.get_height() - (self.screen.get_height() - self.imgSize) / 2),
            )
        )

        if time.time() - self.startTime > 10:
            self.startGameWith = (
                self.images[self.currentSelection],
                stats.GetStats(self.currentSelection)
            )
