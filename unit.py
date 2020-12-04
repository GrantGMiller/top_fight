import math

import pygame
from helpers import rot_center

from physics import Physics


class Unit(Physics):
    def __init__(self, screen, imgPath=None, name=None):
        self.screen = screen
        self.name = name or imgPath
        Physics.__init__(
            self,
            rect=(0, 0, 100, 100),
            initAngularVelocity=3000,
            friction=100,  # acceleration in  per second
            angularFriction=100,  # acceleration in degrees per second
        )
        self.imgBase = pygame.image.load(imgPath or r'parts\1.png')
        self.imgBase = self.imgBase.convert_alpha()
        self.imgBase = pygame.transform.scale(self.imgBase, self.size)
        self.image = self.imgBase

        self.edgeFriction = 100

        self._mask = None
        self._UpdateMask()

    def _UpdateMask(self):
        self.mask = pygame.mask.from_surface(self.image)
        maskRect = self.mask.get_bounding_rects()[0]
        maskRect.center = self.center
        self.maskRect = maskRect

    def BounceOffWalls(self):
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

    def Draw(self, clock):
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
