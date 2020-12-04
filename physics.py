import math
import pygame


class Physics(pygame.Rect):
    def __init__(
            self,
            rect,
            initVelocity=(0, 0),
            initAcceleration=(0, 0),
            initAngularVelocity=0,
            initAngularAcceleration=0,
            friction=0,  # absolute values since friction goes both ways
            angularFriction=0,  # absolute
    ):
        # position
        super().__init__(rect)
        self.position = pygame.Vector2(
            self.center)  # self.center is integer only, this will keep floating point resolution
        self._velocity = pygame.Vector2(
            initVelocity
        )  # pixels per second (or per frame if no "clock" parameter is passed to .Update())
        self._acceleration = pygame.Vector2(initAcceleration)

        # rotation
        self.angle = 0
        self._angularVelocity = initAngularVelocity  # degrees per second (or frame)
        self._angularAcceleration = initAngularAcceleration  # degrees per second (or frame)
        self.deltaAngle = 0

        # friction
        self.friction = math.fabs(friction)
        self.angularFriction = math.fabs(angularFriction)

    @property
    def angularVelocity(self):
        return self._angularVelocity

    @angularVelocity.setter
    def angularVelocity(self, newAngVelocity):
        self._angularVelocity = newAngVelocity

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, newAcceleration):
        self._acceleration = pygame.Vector2(newAcceleration)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, newVelocity):
        self._velocity = pygame.Vector2(newVelocity)

    def ApplyPhysics(self, clock=None):
        if clock:
            deltaTime = (clock.get_time() / 1000)
        else:
            deltaTime = 1

        deltaVelocity = self._velocity * deltaTime

        self.position += deltaVelocity
        self.center = self.position

        if self._velocity.magnitude():
            frictionAcceleration = self._velocity.rotate(180).normalize() * self.friction
            frictionAcceleration *= deltaTime
            self._acceleration += frictionAcceleration

        self._velocity += self._acceleration * deltaTime

        self.deltaAngle = self._angularVelocity * deltaTime
        self.angle += self.deltaAngle

        if self._angularVelocity > 0:
            self._angularVelocity -= self.angularFriction * deltaTime
        elif self._angularVelocity < 0:
            self._angularVelocity += self.angularFriction * deltaTime

        self.angularVelocity += self._angularAcceleration * deltaTime
