import random
from collections import defaultdict

import pygame
from particles import Particle
from unit import Unit


class Equip:
    def __init__(self, screen, img, stats):
        self.screen = screen

        if isinstance(img, str):
            self.img = pygame.image.load(img)
        else:
            self.img = img
        self.img = pygame.transform.scale(self.img, (
            int(self.screen.get_height() / 2),
            int(self.screen.get_height() / 2)
        ))
        self.unit = Unit(self.screen, self.img, showRPM=False)
        self.unit.position = (
            (((self.screen.get_width() / 2) - self.unit.width) / 2) + (self.unit.width / 2),
            ((self.screen.get_height() - self.unit.height) / 2) + (self.unit.height / 2),
        )
        self.unit.angularVelocity = 100
        self.unit.angularFriction = 0

        # self.unit.Equip(WeaponFireStick(self.screen, self.unit))

        self.weaponsTypes = [
            WeaponFireStick
        ]

        # init
        self.current = 0
        self.ready = False
        self.lastInteraction = pygame.time.get_ticks()

        self.previewUnits = {
            # type(weapon): Unit()
        }
        surf = pygame.Surface(self.unit.size)
        pygame.draw.circle(
            surf,
            (100, 100, 100),
            surf.get_rect().center,
            surf.get_width() / 2
        )
        for weaponType in self.weaponsTypes:
            unit = Unit(self.screen, surf, showRPM=False, bounceOffWalls=False)
            unit.angularFriction = 0
            unit.angularVelocity = 100
            unit.Equip(weaponType(self.screen, unit))
            self.previewUnits[weaponType] = unit

    def GetSelection(self):
        d = defaultdict(lambda: 0)
        for equip in self.unit.equipment:
            for key in ['attack', 'defense', 'spin']:
                stats = equip.GetStatDelta()
                d[key] += stats[key]

        return self.img, d, [type(e) for e in self.unit.equipment]

    def Event(self, event):
        if event.type == pygame.KEYDOWN:
            self.lastInteraction = pygame.time.get_ticks()
            if event.key in [pygame.K_KP_ENTER, pygame.K_RETURN]:
                self.ready = True

            elif event.key == pygame.K_SPACE:
                self.unit.ClearEquipment()
                print('current=', self.current)
                print('wetypes=', self.weaponsTypes)
                if 0 <= self.current <= len(self.weaponsTypes) -1:
                    try:
                        weaponType = self.weaponsTypes[self.current]
                        self.unit.Equip(weaponType(self.screen, self.unit))
                    except Exception as e:
                        print(e)

            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                if event.key == pygame.K_UP:
                    self.current += 1
                elif event.key == pygame.K_DOWN:
                    self.current -= 1

    def Draw(self, clock):

        if pygame.time.get_ticks() - self.lastInteraction > 5000:
            # self.ready = True
            pass

        self.screen.fill((0, 0, 0))
        self.unit.ApplyPhysics(clock)

        words = pygame.font.Font(None, int(self.screen.get_height() / 15)).render(
            f'Press SPACEBAR to equip. Press ENTER to start the battle.',
            True,
            (255, 255, 255),
        )
        self.screen.blit(
            words,
            (
                int((self.screen.get_width() - words.get_width()) / 2),
                int(self.screen.get_height() - words.get_height()),
            )
        )

        # draw the weapons
        x = self.screen.get_rect().centerx + (
                (self.screen.get_width() - self.screen.get_rect().centerx) - self.unit.width) / 2
        spacing = 100
        weaponTypes = sorted(list(self.previewUnits.keys()), key=lambda t: t.NAME)
        for index, weaponType in enumerate(weaponTypes):
            previewUnit = self.previewUnits[weaponType]
            previewUnit.position = x, self.screen.get_rect().centery + (spacing * (self.current - index))
            previewUnit.Draw(clock)

            if index == self.current:
                words = pygame.font.Font(None, 36).render(
                    f'{previewUnit.equipment[0].NAME}',
                    True,
                    (255, 255, 255)
                )
                self.screen.blit(
                    words,
                    previewUnit.topright
                )

        # draw the unit preview
        self.unit.Draw(clock)


class WeaponFireStick(pygame.Rect):
    # a stick, both ends on fire
    # increases attach,
    # decreases spin
    COLOR = (255, 0, 0)
    NAME = 'Fire Stick'

    def __init__(self, screen, unit):
        self.screen = screen
        self.unit = unit
        self.particles = []

        self.particlesPerSecond = 100
        self.lastParticle = 0

        self.surf = pygame.Surface((
            int(self.unit.width * 1.1),
            int(self.unit.height / 4),
        ))
        super().__init__(self.surf.get_rect())

        self.ballRadius = int(self.surf.get_height() / 2)
        pygame.draw.line(
            self.surf,
            self.COLOR,
            (0, int(self.surf.get_height() / 2)),
            (self.surf.get_width(), int(self.surf.get_height() / 2)),
            5
        )
        pygame.draw.circle(
            self.surf,
            self.COLOR,
            (
                int(self.surf.get_height() / 2),
                int(self.surf.get_height() / 2),
            ),
            self.ballRadius,
        )
        pygame.draw.circle(
            self.surf,
            self.COLOR,
            (
                int(self.surf.get_width() - (self.surf.get_height() / 2)) + 1,
                int(self.surf.get_height() / 2),
            ),
            self.ballRadius,
        )

        self.surf = self.surf.convert_alpha()

    @staticmethod
    def GetStatDelta():
        return {
            'attack': 10,
            'defense': 0,
            'spin': -10,
        }

    def AddFireParticle(self):
        for delta in [
            self.surf.get_width() / 2,
            0 - (self.surf.get_width() / 2),
        ]:
            relativePos = pygame.Vector2(0, delta) - (0, -self.ballRadius if delta < 0 else self.ballRadius)
            relativePos = relativePos.rotate(-self.unit.angle + 90)
            particle = Particle(
                pos=self.unit.center + relativePos,
                intensity=random.randint(5, 25),
                color=(
                    random.randint(200, 255),
                    random.randint(100, 200),
                    0
                ),
                velocity=(0, 0),
            )
            self.particles.append(particle)

    def Draw(self, clock):

        surf = pygame.transform.rotate(self.surf, self.unit.angle)

        if (pygame.time.get_ticks() - self.lastParticle) / 1000 > 1 / self.particlesPerSecond:
            self.AddFireParticle()
            self.lastParticle = pygame.time.get_ticks()

        self.center = self.unit.center
        self.unit.screen.blit(
            surf,
            (
                (self.unit.centerx - surf.get_width() / 2),
                (self.unit.centery - surf.get_height() / 2),
            ),
            special_flags=pygame.BLEND_RGBA_ADD,
        )

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
