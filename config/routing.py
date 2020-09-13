from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from src.channels_utils.socket_auth_middleware import JWTAuthMiddleware

from src.sessions.consumers import SessionConsumer


application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(
        URLRouter([
            path('api/session/<pk>/', SessionConsumer),
        ])
    ),
})

