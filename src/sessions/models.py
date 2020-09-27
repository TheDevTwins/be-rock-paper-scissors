from django.db import models
from django.db.models import F

from src.channels_utils.functions import send_to_channels_group
from src.players.constants import *

from .constants import *


class Session(models.Model):
    code = models.CharField(max_length=6)
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)

    timer = models.IntegerField(default=0)

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
        self.start_playing()

    def start_waiting(self):
        self.timer = 5
        self.status = WAITING
        self.save()
        self.compute_points()

    def start_playing(self):
        self.players.filter(state=IN_GAME).update(pick=None)
        self.timer = 20
        self.status = PLAYING
        self.save()

    def finish_game(self):
        self.timer = 0
        self.status = FINISHED
        self.save()

    def remove_inactive_players(self):
        self.players.filter(pick=None).update(state=LOST)

    def compute_points(self):
        players = self.players.filter(state=IN_GAME)

        rocks = players.filter(pick=ROCK)
        papers = players.filter(pick=PAPER)
        scissors = players.filter(pick=SCISSORS)

        rocks.update(points=F('points')-papers.count())
        papers.update(points=F('points')-scissors.count())
        scissors.update(points=F('points')-rocks.count())
        players.filter(points__lt=0).update(points=0)

        players.filter(points=0).update(state=LOST)
        players.filter(pick=None).update(state=LOST, points=0)

        players_in_game = players.count()
        if players_in_game == 1:
            players.filter(state=IN_GAME).update(state=WON)
        if players_in_game <= 1:
            self.finish_game()

        reveal = [
            {'player_id': p.id, 'pick': p.pick, 'points': p.points, 'state': p.state} for
            p in self.players.filter(player_type=PLAYER)
        ]
        self.send_to_channels_group('picks_revealed', reveal)
