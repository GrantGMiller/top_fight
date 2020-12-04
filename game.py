import math
import os
import random

import pygame

from particles import Particle
from unit import Unit


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.units = []
        self.gravities = []
        self.particles = []

    def AddUnit(self, unit):
        self.units.append(unit)
        return unit

    def AddRandomUnit(self):
        other = self.AddUnit(Unit(
            self.screen,
            name=f'Name {random.randint(1111, 9999)}',
            imgPath=random.choice(
                ['parts/' + item for item in os.listdir(r'C:\Users\gmiller\PycharmProjects\top_fight\parts')]
            ))
        )
        other.position = (
            random.randint(0, self.screen.get_width()),
            random.randint(0, self.screen.get_height())
        )
        other.velocity = (random.randint(100, 200), random.randint(50, 100))

    def AddGravity(self, pos, strength=1):
        gravity = Gravity(pos, strength)
        print('gravity=', gravity)
        self.gravities.append(gravity)

    def AddParticle(self, *a, **k):
        p = Particle(*a, **k)
        self.particles.append(p)
        return p

    def UnitsBounceOffEachOther(self):
        for unit1 in self.units:
            for unit2 in self.units:
                offset = (
                    unit2.centerx - unit1.centerx,
                    unit2.centery - unit1.centery
                )
                if unit1 != unit2:
                    if unit1.mask.overlap(unit2.mask, offset):
                        reflectVector = (unit1.position - unit2.position).normalize()
                        unit1.Bounce(reflectVector=reflectVector, rotation=False)

                        intensity = int((unit1.velocity.magnitude() + unit2.velocity.magnitude()) / 10)
                        for i in range(random.randint(0, int(intensity / 4))):
                            self.AddParticle(
                                unit1.position,
                                intensity=intensity,
                            )

                        # when 2 units hit each other,
                        #   they should transfer some linear momentum to each other
                        if unit1.velocity.magnitude():
                            totalMag = unit1.velocity.magnitude() + unit2.velocity.magnitude()
                            newVectorNormal = (unit1.velocity.normalize() + reflectVector).normalize()
                            unit1.velocity = newVectorNormal * totalMag / 2

    def Draw(self, clock):

        self.screen.fill((0, 0, 0))

        if len(self.units) == 1:
            print('The winner is', self.units[0].name)
            raise Exception(f'The winner is {self.units[0].name}')

        for gravity in self.gravities:
            pygame.draw.circle(
                self.screen,
                pygame.color.Color((50, 50, 50)),
                gravity.center,
                gravity.strength / 2,
            )

        for unit in self.units:

            if math.fabs(unit.angularVelocity < 40):
                print('unit', unit.name, 'is dead')
                self.units.remove(unit)

                for i in range(500 - len(self.particles)):
                    intensity = random.randint(10, 300)
                    if intensity > 250:
                        intensity *= 3

                    self.AddParticle(
                        unit.position,
                        intensity=intensity,
                        color=pygame.Color((
                            random.randint(0, 100),
                            random.randint(0, 100),
                            random.randint(100, 255),
                        )),
                    )
                self.AddRandomUnit()
                continue  # this unit is dead

            totalGravity = pygame.Vector2(0, 0)
            for gravity in self.gravities:
                distance = pygame.Vector2(
                    gravity.center) - pygame.Vector2(unit.center)

                if distance.magnitude():
                    gravityVector = distance.normalize() * gravity.strength
                    totalGravity += gravityVector

            unit.acceleration = totalGravity
            unit.Draw(clock)

        self.UnitsBounceOffEachOther()

        for particle in self.particles:
            if particle.lifespan <= 0:
                self.particles.remove(particle)

            particle.Update(clock)
            pygame.draw.circle(
                self.screen,
                particle.color,
                particle.position,
                particle.size,
            )

    def Event(self, event):
        pass


class Gravity(pygame.Rect):
    def __init__(self, pos, strength):
        super().__init__(pos[0], pos[1], 1, 1)
        self.strength = strength
