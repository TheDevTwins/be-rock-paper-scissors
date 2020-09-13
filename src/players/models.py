from django.db import models

from .constants import *


class Avatar(models.Model):
    hat = models.PositiveSmallIntegerField(default=0)
    face = models.PositiveSmallIntegerField(default=0)
    skin = models.PositiveSmallIntegerField(default=0)
    shirt = models.PositiveSmallIntegerField(default=0)


class Player(models.Model):
    session = models.ForeignKey('sessions.Session', related_name='players', on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    player_type = models.PositiveIntegerField(choices=PLAYER_TYPES, default=SPECTATOR)
    is_admin = models.BooleanField(default=False)

    avatar = models.OneToOneField(Avatar, on_delete=models.CASCADE)

