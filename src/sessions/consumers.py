from random import randrange

from asgiref.sync import async_to_sync
from channels.consumer import StopConsumer

from src.channels_utils.consumers import GenericApiConsumer
from src.players.models import Player, Avatar
from src.players.serializers import PlayerSerializer

from .models import Session


class SessionConsumer(GenericApiConsumer):
    queryset = Session.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None

    def connect(self):
        super().connect()
        session = self.get_object()
        is_admin = session.players.count() == 0
        name = f'Guest #{randrange(1000, 9999)}'

        avatar = Avatar.objects.create()
        self.player = Player.objects.create(name=name, session=session, is_admin=is_admin, avatar=avatar)

        async_to_sync(self.channel_layer.group_add)(session.channels_group_name, self.channel_name)
        session.send_to_channels_group('player_joined', PlayerSerializer(self.player).data)

    def disconnect(self, close_code):
        session = self.get_object()

        session.send_to_channels_group('player_left', {'id': self.player.id})
        self.player.delete()

        async_to_sync(self.channel_layer.group_discard)(session.channels_group_name, self.channel_name)
        raise StopConsumer

    def receive_json(self, content, **kwargs):
        pass

    def session_updated(self, event):
        self.send_json(event)

    def player_joined(self, event):
        self.send_json(event)

    def player_left(self, event):
        self.send_json(event)
