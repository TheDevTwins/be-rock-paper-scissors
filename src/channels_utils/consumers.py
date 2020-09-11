from channels.exceptions import DenyConnection
from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import QuerySet, ObjectDoesNotExist

from .settings import channels_settings


class GenericApiConsumer(JsonWebsocketConsumer):
    permission_classes = channels_settings.DEFAULT_PERMISSION_CLASSES
    queryset = None
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.scope['url_route']['kwargs'], (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.scope['url_route']['kwargs'][lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except ObjectDoesNotExist:
            raise DenyConnection()

        # May raise a permission denied
        self.check_object_permissions(obj)

        return obj

    def check_permissions(self):
        for permission in [permission() for permission in self.permission_classes]:
            if not permission.has_permission(self.scope):
                raise DenyConnection()

    def check_object_permissions(self, obj):
        for permission in [permission() for permission in self.permission_classes]:
            if not permission.has_object_permission(self.scope, obj):
                raise DenyConnection()

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data == 'PING':
            self.send('PONG')
        elif text_data:
            self.receive_json(self.decode_json(text_data), **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    def connect(self):
        self.check_permissions()
        super().connect()
