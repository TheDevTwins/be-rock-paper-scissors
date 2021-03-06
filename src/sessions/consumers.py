from random import randrange

from asgiref.sync import async_to_sync
from channels.consumer import StopConsumer

from src.channels_utils.consumers import GenericApiConsumer
from src.players.models import Player, Avatar
from src.players.constants import PLAYER
from src.players.serializers import PlayerSerializer, AvatarSerializer

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

        was_admin = self.player.is_admin

        session.send_to_channels_group('player_left', {'id': self.player.id})
        self.player.delete()

        try:
            if was_admin:
                new_admin = session.players.first()
                new_admin.is_admin = True
                new_admin.save()

                session.send_to_channels_group('admin_updated', {'player_id': new_admin.id})
        except:
            pass

        async_to_sync(self.channel_layer.group_discard)(session.channels_group_name, self.channel_name)
        raise StopConsumer

    def receive_json(self, content, **kwargs):
        action = content.get('type')
        data = content.get('data')

        session = self.get_object()
        player = self.player

        if action == 'update_avatar':
            serializer = AvatarSerializer(player.avatar, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            session.send_to_channels_group('avatar_updated', {'player_id': player.id, 'avatar': serializer.data})
        elif action == 'update_name':
            name = data.get('name')
            player.name = name
            player.save()

            session.send_to_channels_group('name_updated', {'player_id': player.id, 'name': name})
        elif action == 'update_player_type':
            player_type = data.get('player_type')
            player.player_type = player_type
            player.save()

            session.send_to_channels_group('player_type_updated', {'player_id': player.id, 'player_type': player_type})
        elif action == 'send_message':
            message = data.get('message')

            session.send_to_channels_group('message_received', {'message': message, 'player_id': player.id})
        elif action == 'start_game':
            if not player.is_admin:
                return

            session.start_game()
            session.send_to_channels_group('game_started')
        elif action == 'make_pick':
            player.pick = data.get('pick')
            player.save()

            session.send_to_channels_group('player_picked', {'player_id': player.id})

            if session.players.filter(pick=None, player_type=PLAYER).count() == 0:
                session.start_waiting()

    def session_updated(self, event):
        self.send_json(event)

    def player_joined(self, event):
        self.send_json(event)

    def player_left(self, event):
        self.send_json(event)

    def avatar_updated(self, event):
        self.send_json(event)

    def name_updated(self, event):
        self.send_json(event)

    def player_type_updated(self, event):
        self.send_json(event)

    def message_received(self, event):
        self.send_json(event)

    def game_started(self, event):
        self.send_json(event)

    def player_picked(self, event):
        self.send_json(event)

    def picks_revealed(self, event):
        self.send_json(event)

    def timer_updated(self, event):
        self.send_json(event)

    def admin_updated(self, event):
        self.send_json(event)

    def started_playing(self, event):
        self.send_json(event)

    def started_waiting(self, event):
        self.send_json(event)
