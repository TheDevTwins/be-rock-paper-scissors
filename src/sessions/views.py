from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Session
from .serializers import SessionSerializer
from .constants import FINISHED, PLAYING


class SessionViewSet(CreateModelMixin, GenericViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = []