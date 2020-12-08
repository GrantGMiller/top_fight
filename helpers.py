import random
import string
import uuid
import hashlib

import pygame


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def GetRandomColor(x=None):
    x = x or uuid.uuid4()
    colorString = hashlib.sha256(str(x).encode()).hexdigest()
    return pygame.color.Color(f'#{colorString[:6]}')


def GetRandomValue(x=None, maxi=100):
    x = x or uuid.uuid4()
    v = hashlib.sha256(str(x).encode()).hexdigest()[:32]
    print('v=', v)
    b = bytes.fromhex(v)
    print('b=', b)
    ret = int.from_bytes(b, 'big') % maxi
    print('ret=', ret)
    return ret
