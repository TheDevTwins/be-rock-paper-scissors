from asgiref.sync import async_to_sync
from channels.consumer import StopConsumer

from src.channels_utils.consumers import GenericApiConsumer
from src.channels_utils.permissions import IsAuthenticated, IsInSession
from .models import Session


class SessionConsumer(GenericApiConsumer):
    queryset = Session.objects.all()
    permission_classes = (IsAuthenticated, IsInSession)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None
        self.player_id = None

    def connect(self):
        super().connect()
        self.player = self.get_object().players.get(user=self.scope['user'])
        self.player_id = self.player.id
        session = self.get_object()
        async_to_sync(self.channel_layer.group_add)(session.channels_group_name, self.channel_name)

    def disconnect(self, close_code):
        session = self.get_object()
        async_to_sync(self.channel_layer.group_discard)(session.channels_group_name, self.channel_name)
        raise StopConsumer

    def session_updated(self, event):
        self.send_json(event)
