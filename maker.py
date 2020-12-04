import time

import pygame


class Maker:
    def __init__(self, screen):
        self.screen = screen
        self.surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.lineColor = pygame.color.Color('white')
        self.lineThickness = 6
        self.lastMousePoint = None

    def Event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.CreateImage()

    def CreateImage(self):
        with open(f'parts/test.tga', mode='wb') as file:
            pygame.image.save(self.surf, file)

    def MirrorPoint(self, pos):
        middleXtoPx = pos[0] - self.screen.get_width() / 2
        ret0 = self.screen.get_width() / 2 - middleXtoPx

        middleYtoPy = pos[1] - self.screen.get_height() / 2
        ret1 = self.screen.get_height() / 2 - middleYtoPy
        return ret0, ret1

    def DrawMirror(self, startPos, endPos):
        if startPos:
            pygame.draw.line(
                self.surf,
                self.lineColor,
                self.MirrorPoint(startPos),
                self.MirrorPoint(endPos),
                self.lineThickness,
            )
        else:
            pygame.draw.circle(
                self.surf,
                self.lineColor,
                self.MirrorPoint(endPos),
                self.lineThickness / 2,
            )

    def Draw(self, clock):
        # draw a line down the middle (the part will be symetrical)
        self.screen.fill((0, 0, 0))

        pygame.draw.line(
            self.screen,
            pygame.color.Color('grey'),
            (self.screen.get_width() / 2, 0),
            (self.screen.get_width() / 2, self.screen.get_height()),
            1,
        )
        pygame.draw.line(
            self.screen,
            pygame.color.Color('grey'),
            (0, self.screen.get_height() / 2),
            (self.screen.get_width(), self.screen.get_height() / 2),
            1
        )

        # draw new lines
        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            if self.lastMousePoint:
                pygame.draw.line(
                    self.surf,
                    self.lineColor,
                    self.lastMousePoint,
                    mousePos,
                    self.lineThickness,
                )
                self.DrawMirror(
                    startPos=self.lastMousePoint,
                    endPos=mousePos,
                )
            else:
                pygame.draw.circle(
                    self.surf,
                    self.lineColor,
                    mousePos,
                    self.lineThickness / 2,
                )
                self.DrawMirror(
                    startPos=None,
                    endPos=mousePos,
                )

            self.lastMousePoint = mousePos

        else:
            self.lastMousePoint = None

        self.screen.blit(self.surf, (0, 0))
