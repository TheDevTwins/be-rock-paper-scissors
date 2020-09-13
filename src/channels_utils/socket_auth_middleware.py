from urllib.parse import parse_qsl

from django.db import close_old_connections


class SocketAuthMiddleware:
    """
    JWT authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        # scope['params'] = dict(parse_qsl(scope['query_string'].decode()))

        return self.inner(scope)
