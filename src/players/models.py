from django.db import models

from .constants import *


class Player(models.Model):
    session = models.ForeignKey('sessions.Session', on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    player_type = models.PositiveIntegerField(choices=PLAYER_TYPES, default=SPECTATOR)
    is_admin = models.BooleanField(default=False)
