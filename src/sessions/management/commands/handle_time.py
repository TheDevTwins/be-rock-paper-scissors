import time

from django.core.management.base import BaseCommand

from src.sessions.models import Session
from src.sessions.constants import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            for session in Session.objects.filter(status=PLAYING):
                if session.timer:
                    session.timer -= 1
                    session.save()
                    session.send_to_channels_group('timer_updated', {'value': session.timer})
                else:
                    session.start_waiting()
            for session in Session.objects.filter(status=WAITING):
                if session.timer:
                    session.timer -= 1
                    session.save()
                    session.send_to_channels_group('timer_updated', {'value': session.timer})
                else:
                    session.start_playing()
            time.sleep(1)
