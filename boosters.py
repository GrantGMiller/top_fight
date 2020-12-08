import random

import pygame

from physics import Physics


class _BaseBooster(Physics):
    def __init__(self, pos, game):
        self.pos = pos  # center
        self.game = game
        self.radius = 10  # radius

        super().__init__(
            rect=(
                self.pos[0] - self.radius,
                self.pos[1] - self.radius,
                self.radius * 2,
                self.radius * 2
            ),

        )

        if not hasattr(self, 'color'):
            self.color = pygame.color.Color((255, 255, 255))
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(
            self.surf,
            self.color,
            (0 + self.radius, 0 + self.radius),
            self.radius,
        )
        self.mask = pygame.mask.from_surface(self.surf)
        self.done = False

    def Activate(self, unit):
        for i in range(random.randint(5, 10)):
            self.game.AddParticle(
                pos=self.pos,
                intensity=10,
                color=pygame.color.Color((255, 255, 0))
            )

    def Done(self):
        self.done = True

    def Draw(self, screen):
        screen.blit(
            self.surf,
            (
                self.pos[0] - self.radius,
                self.pos[1] - self.radius,
            )
        )
        self.game.AddParticle(
            pos=self.pos,
            intensity=1,
            color=self.color,
        )


class SpinBooster(_BaseBooster):
    def __init__(self, pos, game):
        self.color = pygame.color.Color((255, 127, 127))
        super().__init__(pos, game)

    def Activate(self, unit):
        super().Activate(unit)

        unit.angularVelocity *= 2

        for dir in range(0, 360, 5):
            delta = pygame.Vector2(unit.width, 0).rotate(dir)
            self.game.AddParticle(
                pos=unit.center,
                intensity=20,
                velocity=delta.rotate(-90) * 15,
                friction=0,
                color=self.color
            )

        self.Done()


class VelocityBooster(_BaseBooster):
    def __init__(self, *a, **k):
        self.color = pygame.color.Color((127, 255, 127))
        super().__init__(*a, **k)

    def Activate(self, unit):
        super().Activate(unit)
        unit.velocity *= 2
        if unit.velocity.magnitude() < 300:
            unit.velocity = unit.velocity.normalize() * 300

        for i in range(25):
            self.game.AddParticle(
                pos=unit.center,
                intensity=20,
                velocity=unit.velocity.rotate(180 + random.randint(-30, 30)),
                friction=0,
                color=self.color
            )

        self.Done()


class GravityBooster(_BaseBooster):
    def __init__(self, *a, **k):
        self.color = pygame.color.Color((127, 127, 255))
        self.life = random.randint(200, 300)
        self.gravity = None
        super().__init__(*a, **k)

    def Activate(self, unit):
        if self.gravity is None:
            print('GravityBooster.Activate(', unit)
            super().Activate(unit)
            self.gravity = self.game.AddGravity(
                pos=self.pos,
                strength=500,
                color=pygame.color.Color('black'),
            )

    def Decrement(self):
        if self.gravity:
            self.life -= 1

            dir = random.randint(0, 359)
            delta = pygame.Vector2(self.gravity.strength / 2.2, 0).rotate(dir)
            pos = delta + self.pos
            self.game.AddParticle(
                pos=pos,
                intensity=2,
                velocity=delta.rotate(180) * 3,
                friction=0,
                color=self.color
            )

            if self.life <= 0:
                self.game.gravities.remove(self.gravity)
                self.Done()

    def Draw(self, screen):
        super().Draw(screen)
        self.Decrement()
