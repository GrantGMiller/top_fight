import math
import os
import random

import pygame

from boosters import SpinBooster, VelocityBooster, GravityBooster
from particles import Particle
from unit import Unit


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.sidebarWidth = 0  # max(200, int(screen.get_width() / 7))
        self.surf = screen.subsurface(
            (
                self.sidebarWidth,
                0,
                screen.get_width() - self.sidebarWidth,
                screen.get_height()
            )
        )
        self.units = []
        self.gravities = []
        self.particles = []
        self.boosters = []

        self.player = None

        self.gameOver = False

    def NewGame(self, img=None, stats=None, numUnits=None, name=None):
        if img:
            unit = self.AddUnit(
                Unit(
                    self.screen,
                    imgPath=img,
                    highlight=True,
                    name=name,
                )
            )
            unit.angularVelocity += stats.get('spin', 0) * 10
            self.player = unit

        for i in range(numUnits or int(self.surf.get_width() / 300) + 2):
            self.AddRandomUnit()

        self.AddGravity(self.surf.get_rect().center, random.randint(50, 100))
        for i in range(random.randint(4, int(self.screen.get_width() / 100))):
            self.AddGravity(
                (
                    random.randint(0, self.surf.get_width()),
                    random.randint(0, self.surf.get_height())
                ),
                random.randint(10, 25),
            )
        self.AddRandomBooster()

    def AddUnit(self, unit):
        self.units.append(unit)
        return unit

    def AddRandomUnit(self, **k):
        other = self.AddUnit(
            Unit(
                self.surf,
                imgPath=random.choice(
                    ['parts/' + item for item in os.listdir(r'C:\Users\gmiller\PycharmProjects\top_fight\parts')]
                ),
                **k
            ),
        )
        other.position = (
            random.randint(0, self.surf.get_width()),
            random.randint(0, self.surf.get_height())
        )
        other.velocity = (random.randint(100, 200), random.randint(50, 100))
        return other

    def AddBooster(self, booster):
        self.boosters.append(booster)
        return booster

    def AddRandomBooster(self):
        boosterType = random.choice([
            SpinBooster,
            VelocityBooster,
            GravityBooster,
        ])
        w, h = self.surf.get_size()
        booster = boosterType(
            (
                random.randint(int(0 + w / 4), int(3 * w / 4)),
                random.randint(int(0 + h / 4), int(3 * h / 4)),
            ),
            self,
        )
        self.boosters.append(booster
                             )
        return booster

    def AddGravity(self, pos, strength=1, color=None):
        gravity = Gravity(pos, strength, color)
        print('gravity=', gravity)
        self.gravities.append(gravity)
        return gravity

    def AddParticle(self, *a, **k):
        p = Particle(*a, **k)
        self.particles.append(p)
        return p

    def Collision(self, unit1, unit2):
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

        # when 2 units hit, they should have their angularVelocity decreased
        delta = math.fabs(unit1.angularVelocity - unit2.angularVelocity)
        unit1.angularVelocity -= delta / 4
        unit1.angularVelocity -= delta / 4

    def UnitsBounceOffEachOther(self):
        collisions = []
        for unit1 in self.units:
            for unit2 in self.units:
                offset = (
                    unit2.left - unit1.left,
                    unit2.top - unit1.top
                )
                if unit1 != unit2:
                    if unit1.mask.overlap(unit2.mask, offset):
                        tup = (unit1, unit2)
                        if tup not in collisions:
                            collisions.append(tup)

        for collision in collisions:
            self.Collision(*collision)

    def DrawSideBar(self):
        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            (
                0,
                0,
                self.sidebarWidth,
                self.surf.get_height(),
            )
        )

        yOffset = 25
        spacer = 10
        fontHeight = int(self.screen.get_height() / 20)

        def WriteText(text, size, color=(255, 255, 255)):
            nonlocal yOffset
            size = int(size)
            f = pygame.font.Font(None, size)
            s = f.render(text, True, color)
            self.screen.blit(
                s,
                (
                    (self.sidebarWidth - s.get_width()) / 2,
                    yOffset,
                )
            )

            yOffset += s.get_height() + spacer

        for unit in sorted(self.units, key=lambda u: u.rpm):
            WriteText(unit.name, fontHeight)
            WriteText(f'RPM {unit.rpm}', fontHeight * 0.9,
                      (255, 0, 0) if unit.angularVelocity < unit.angVelocityLimit else (255, 255, 255))

    def Draw(self, clock):

        self.surf.fill((0, 0, 0))

        if len(self.units) == 1:
            self.gameOver = True

        for gravity in self.gravities:
            pygame.draw.circle(
                self.surf,
                gravity.color,
                gravity.center,
                gravity.strength / 2,
            )

        for booster in self.boosters:
            if booster.done is True:
                self.boosters.remove(booster)
                self.AddRandomBooster()
            else:
                booster.Draw(self.surf)

        for unit in self.units:
            for booster in self.boosters:

                offset = (
                    unit.centerx - booster.centerx + booster.width * 2,
                    unit.centery - booster.centery + booster.width * 2
                )
                if unit.mask.overlap(booster.mask, offset):
                    print('booster=', booster.mask)
                    print('unit=', unit.mask)
                    booster.Activate(unit)
                    break

            if math.fabs(unit.angularVelocity < 90) and not self.gameOver:
                print('unit', unit.name, 'is dead')
                self.units.remove(unit)

                explodeColor = pygame.transform.average_color(unit.imgBase)

                for i in range(500 - len(self.particles)):
                    intensity = random.randint(10, 300)
                    if intensity > 250:
                        intensity *= 3

                    self.AddParticle(
                        unit.position,
                        intensity=intensity,
                        color=pygame.Color((
                            max(0, min(255, explodeColor[0] + random.randint(-25, 25))),
                            max(0, min(255, explodeColor[1] + random.randint(-25, 25))),
                            max(0, min(255, explodeColor[2] + random.randint(-25, 25))),
                        )),
                    )
                # self.AddRandomUnit()
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
                self.surf,
                particle.color,
                particle.position,
                particle.size,
            )

        if self.sidebarWidth:
            self.DrawSideBar()

    def Event(self, event):
        pass


class Gravity(pygame.Rect):
    def __init__(self, pos, strength, color=None):
        super().__init__(pos[0], pos[1], 1, 1)
        self.strength = strength
        self.color = color or pygame.color.Color((50, 50, 50))
