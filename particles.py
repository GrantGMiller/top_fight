import random

import pygame

from physics import Physics


class Particle(Physics):
    MAX_PARTICLE_SIZE = 10

    def __init__(self, pos, intensity=None, color=None, velocity=None, friction=None, gravity=None):
        intensity = intensity or random.randint(5, 25)
        self.color = color or pygame.color.Color((
            random.randint(200, 255),
            random.randint(200, 255),
            255,
            127,# alpha
        ))
        self.lifespan = intensity / 10  # seconds
        self.lifespan = min(0.5, self.lifespan) + random.randint(-10, 10) / 10
        super().__init__(
            rect=(pos[0], pos[1], self.lifespan / 2, self.lifespan / 2),
            initVelocity=velocity or (
                random.randint(-25, 25) * intensity,
                random.randint(-25, 25) * intensity,
            ),
            friction=0,
        )
        self.position = pygame.Vector2(pos)

    def Update(self, clock):
        self.ApplyPhysics(clock)
        self.lifespan -= clock.get_time() / 1000

    @property
    def size(self):
        return min(self.MAX_PARTICLE_SIZE, self.lifespan * 10)
