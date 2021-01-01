import math
import random
import pygame
from physics import Physics


class Unit(Physics):
    def __init__(self, screen, img=None, name=None, highlight=False, showRPM=True, equipment=None, bounceOffWalls=True):
        self.screen = screen
        self.name = name or f'Name {random.randint(1111, 9999)}'
        self.highlight = highlight
        self.showRPM = showRPM
        self.equipment = equipment or []
        self.bounceOffWalls = bounceOffWalls

        Physics.__init__(
            self,
            rect=(0, 0, 100, 100),
            initAngularVelocity=3000,
            friction=0,  # acceleration in  per second
            angularFriction=100,  # acceleration in degrees per second
        )
        if isinstance(img, str):
            self.imgBase = pygame.image.load(img or r'parts\1.png')
        else:
            self.imgBase = img

        self.imgBase = self.imgBase.convert_alpha()
        self.imgBase = pygame.transform.scale(self.imgBase, self.size)
        self.image = self.imgBase

        self.edgeFriction = 100

        self._mask = None
        self.angVelocityLimit = 500
        self._UpdateMask()

        self.font = pygame.font.Font(None, 16) if not self.highlight else pygame.font.Font(None, 32)
        self.fontColor = pygame.color.Color('white') if not self.highlight else pygame.color.Color('cyan')

        avgColor = pygame.transform.average_color(self.imgBase)
        font = pygame.font.Font(None, int(self.height / 3))
        self.surfTitle = font.render(self.name, True, avgColor)

    def Equip(self, weapon):
        self.equipment.append(weapon)

    def ClearEquipment(self):
        self.equipment.clear()

    def _UpdateMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        maskRect = self.mask.get_bounding_rects()[0]
        maskRect.center = self.center
        self.maskRect = maskRect

        if self.angularVelocity < self.angVelocityLimit:
            size = self.angVelocityLimit - self.angularVelocity
            size = max(12, size)
            size = min(48, size)
            self.font = pygame.font.Font(None, int(size))

    def BounceOffWalls(self):
        if self.bounceOffWalls:
            screenRect = self.screen.get_rect()
            # when an object bounces off a wall, it should pickup or lose angular momentum

            # bounce off wall
            bounceVector = pygame.Vector2(0, 0)

            if self.maskRect.left <= screenRect.left:
                bounceVector += pygame.Vector2(1, 0)

            elif self.maskRect.right >= screenRect.right:
                bounceVector += pygame.Vector2(-1, 0)

            if self.maskRect.top <= screenRect.top:
                bounceVector += pygame.Vector2(0, 1)

            elif self.maskRect.bottom >= screenRect.bottom:
                bounceVector += pygame.Vector2(0, -1)

            self.KeepInBounds()
            if bounceVector:
                self.Bounce(reflectVector=bounceVector)

    def KeepInBounds(self):
        if self.bounceOffWalls:
            # self.position is the center (for some reason, im sorry)
            if self.maskRect.left < self.screen.get_rect().left:
                self.position = (
                    self.screen.get_rect().left + self.maskRect.width / 2 + 1,
                    self.position[1]
                )

            elif self.maskRect.right > self.screen.get_rect().right:
                self.position = (
                    self.screen.get_rect().right - self.maskRect.width / 2 - 1,
                    self.position[1]
                )

            if self.maskRect.top < self.screen.get_rect().top:
                self.position = (
                    self.position[0],
                    self.screen.get_rect().top + self.maskRect.height / 2 + 1,
                )

            elif self.maskRect.bottom > self.screen.get_rect().bottom:
                self.position = (
                    self.position[0],
                    self.screen.get_rect().bottom - self.maskRect.height / 2 - 1,
                )

    def Bounce(self, x=False, y=False, reflectVector=None, rotation=True):
        if reflectVector:
            if rotation and self.velocity.magnitude():
                # add the x component of the reflectVector to the angular velocity

                # get the resulting vector - the accounts for what angle the unit strikes the wall
                rotationVector = self.velocity.normalize() + reflectVector

                # flip the rotation vector 180 deg because the force on the unit will be in the opposite direction
                rotationVector = rotationVector.rotate(180)

                # we know the direction of the rotation vector, but this will make
                #   the unit spin in different directions depending on if the
                #   rotationVector is applied to the left/right/top/bottom side

                # We can use the cross product between the reflectVector and the rotaionVector
                #   to determine if the rotaion should be anti/clockwise
                cross = reflectVector.cross(rotationVector)
                WALL_FRICTION = 3
                deltaAngVelocity = cross * self.angularFriction
                self.angularVelocity += deltaAngVelocity * WALL_FRICTION

                # reduce the linear velocity (cuz that rotational energy has to go somewhere
                self.velocity -= self.velocity.normalize() * math.fabs(deltaAngVelocity)

            # reflectVector is the direction of the normal force from the wall/object
            self.velocity = self.velocity.reflect(reflectVector)

        else:
            if x:
                self.velocity = (
                    -self.velocity[0],
                    self.velocity[1],
                )
            if y:
                self.velocity = (
                    self.velocity[0],
                    -self.velocity[1],
                )

    @property
    def rpm(self):
        return int(self.angularVelocity * 60 / 360)

    def Rotate(self):
        oldCenter = self.center
        self.image = pygame.transform.rotate(self.imgBase, self.angle)
        self.center = oldCenter

    def DrawHighlight(self):
        if self.highlight:
            self.screen.blit(
                self.surfTitle,
                (
                    self.centerx - self.surfTitle.get_width() / 2,
                    self.top - self.surfTitle.get_height(),
                )
            )

    def Draw(self, clock):
        # limit the rotation
        self.angularVelocity = min(100000, self.angularVelocity)

        # limit speed
        if self.velocity.magnitude() > 10000:
            self.velocity = self.velocity.normalize() * 10000

        self.Rotate()
        self._UpdateMask()
        self.BounceOffWalls()
        self.ApplyPhysics(clock)
        self._UpdateMask()
        self.screen.blit(
            self.image,
            (
                self.center[0] - self.image.get_width() / 2,
                self.center[1] - self.image.get_height() / 2,
            )
        )

        # draw equipment
        for equip in self.equipment:
            equip.Draw(clock)

        # draw the rpm heads up
        if self.showRPM:
            wordSurface = self.font.render(
                f'{self.rpm}',
                True,
                self.fontColor if self.angularVelocity > self.angVelocityLimit else pygame.color.Color(
                    'red')
            )
            if math.fabs(self.angularVelocity) < self.angVelocityLimit / 10:
                self.velocity *= 0.95

            self.screen.blit(
                wordSurface,
                self.topleft,
            )

        self.DrawHighlight()
