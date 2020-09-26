from django.db import models
from django.db.models import F

from src.channels_utils.functions import send_to_channels_group
from src.players.constants import *

from .constants import *


class Session(models.Model):
    code = models.CharField(max_length=6)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)

    @staticmethod
    def get_channels_group_name(session_id):
        return f'session_{session_id}'

    @property
    def channels_group_name(self):
        return self.get_channels_group_name(self.id)

    def send_to_channels_group(self, event_type: str, data: any, additional=None):
        if additional is None:
            additional = {}
        send_to_channels_group(self.channels_group_name, {'type': event_type, 'data': data, **additional})

    def start_game(self):
        self.status = PLAYING
        self.save()

    def compute_points(self):
        players = self.players.all()

        rocks = players.filter(pick=ROCK)
        papers = players.filter(pick=PAPER)
        scissors = players.filter(pick=SCISSORS)

        rocks.update(points=F('points')-papers.count())
        papers.update(points=F('points')-scissors.count())
        scissors.update(points=F('points')-rocks.count())
