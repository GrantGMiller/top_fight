import math
import time

import pygame


class Winner:
    def __init__(self, winner, screen):
        self.winner = winner
        self.screen = screen
        self.period = 2  # seconds
        self.angle = 0
        self.imgBase = pygame.transform.scale(
            winner.imgBase,
            (
                int(screen.get_width() / 3),
                int(screen.get_width() / 3)
            )
        )
        self.surfTitle = pygame.font.Font(None, int(screen.get_width() / 4)).render(
            'WINNER',
            True,
            pygame.color.Color('white'),
        )

    def Event(self, event):
        pass

    def Draw(self, clock):
        self.screen.fill((0, 0, 0))
        deltaTime = clock.get_time() / 100
        width = int(self.screen.get_width() / 2 + math.sin(self.period * time.time()))
        self.angle += deltaTime
        surf = pygame.transform.rotate(self.imgBase, self.angle)
        self.screen.blit(
            surf,
            (
                int(self.screen.get_rect().centerx - surf.get_width() / 2),
                int(self.screen.get_rect().centery - surf.get_height() / 2) + 100,
            )
        )

        self.screen.blit(
            self.surfTitle,
            (
                int(self.screen.get_width() / 2 - self.surfTitle.get_width() / 2),
                0,
            )
        )
