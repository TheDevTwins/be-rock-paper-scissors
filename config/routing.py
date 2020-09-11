from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from src.channels_utils.socket_auth_middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(
        URLRouter([

        ])
    ),
})

