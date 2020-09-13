import datetime
import jwt
from django.conf import settings

from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.players.models import Player
from src.players.serializers import PlayerSerializer

from .models import Session
from .serializers import SessionSerializer
from .constants import FINISHED, PLAYING


class SessionViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = []

    @action(methods=['POST'], detail=True)
    def join(self, request, *args, **kwargs):
        session = self.get_object()
        username = request.data.get('username', 'Guest')

        is_admin = session.players.count() == 0
        player = Player.objects.create(name=username, is_admin=is_admin, session=session)

        access_token_payload = {
            'player_id': player.id,
            'is_admin': player.is_admin,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload,
                                  settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        return Response(access_token)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        players = instance.players.all()

        return Response({
            'session': self.get_serializer(instance).data,
            'players': PlayerSerializer(players, many=True).data
        })
