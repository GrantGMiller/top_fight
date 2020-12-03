import pygame


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.units = []
        self.gravities = []

    def AddUnit(self, unit):
        self.units.append(unit)
        return unit

    def AddGravity(self, pos, strength=1):
        gravity = Gravity(pos, strength)
        print('gravity=', gravity)
        self.gravities.append(gravity)

    def Draw(self, clock):
        for gravity in self.gravities:
            pygame.draw.circle(
                self.screen,
                pygame.color.Color('blue'),
                gravity.center,
                gravity.strength / 2,
            )

        for unit in self.units:
            totalGravity = pygame.Vector2(0, 0)
            for gravity in self.gravities:
                distance = pygame.Vector2(
                    gravity.center) - pygame.Vector2(unit.center)

                if distance.magnitude():
                    gravityVector = distance.normalize() * gravity.strength
                    totalGravity += gravityVector

            unit.acceleration = totalGravity
            unit.Draw(clock)


class Gravity(pygame.Rect):
    def __init__(self, pos, strength):
        super().__init__(pos[0], pos[1], 1, 1)
        self.strength = strength
