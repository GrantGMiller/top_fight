import pygame


class Maker:
    def __init__(self, screen):
        self.screen = screen
        self.subsurf = self.screen.subsurface(
            self.screen.get_rect(),
        )

    def Event(self, event):
        pass

    def Draw(self):
        # draw a line down the middle (the part will be symetrical)
        pygame.draw.line(
            self.screen,
            pygame.color.Color('white'),
            (self.screen.get_width() / 2, 0),
            (self.screen.get_width() / 2, self.screen.get_height()),
        )

        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(
                self.subsurf,
                pygame.color.Color('white'),
                pygame.mouse.get_pos(),
                3,
            )

