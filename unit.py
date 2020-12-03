import pygame
from helpers import rot_center

from physics import Physics


class Unit(Physics):
    def __init__(self, screen):
        self.screen = screen
        super().__init__(
            rect=(0, 0, 100, 100),
            initAngularVelocity=3000,
            friction=100,
            angularFriction=10,
        )
        self.imgBase = pygame.image.load(r'parts\1.png')
        self.imgBase = self.imgBase.convert_alpha()
        self.imgBase = pygame.transform.scale(self.imgBase, self.size)
        self.img = self.imgBase

        self.edgeFriction = 100

    def BounceOffWalls(self):
        maskRect = pygame.mask.from_surface(self.img).get_bounding_rects()[0]
        maskRect.center = self.center
        # maskRect = mask.get_rect(center=self.center)
        screenRect = self.screen.get_rect()

        # when an object bounces off a wall, it should pickup or lose angular momentum
        
        # bounce off wall
        if maskRect.left <= screenRect.left:
            self.Bounce(x=True)
            self.left = screenRect.left

        elif maskRect.right >= screenRect.right:
            self.Bounce(x=True)
            self.right = screenRect.right

        if maskRect.top <= screenRect.top :
            self.Bounce(y=True)
            self.top = screenRect.top

        elif maskRect.bottom >= screenRect.bottom:
            self.Bounce(y=True)
            self.bottom = screenRect.bottom

    def Bounce(self, x=False, y=False):
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

    def Rotate(self):
        oldCenter = self.center
        self.img = pygame.transform.rotate(self.imgBase, self.angle)
        self.center = oldCenter

    def Draw(self, clock):
        self.Rotate()
        self.ApplyPhysics(clock)
        self.BounceOffWalls()

        self.screen.blit(
            self.img,
            (
                self.center[0] - self.img.get_width() / 2,
                self.center[1] - self.img.get_height() / 2,
            )
        )
