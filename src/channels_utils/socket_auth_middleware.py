from urllib.parse import parse_qsl
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class JWTAuthenticationFromScope(BaseJSONWebTokenAuthentication):
    """
    Extracts the JWT from a channel scope (instead of an http request)
    """

    def get_jwt_value(self, scope):
        try:
            params_map = dict(parse_qsl(scope['query_string'].decode()))
            return params_map['token']
        except KeyError:
            return None


class JWTAuthMiddleware(BaseJSONWebTokenAuthentication):
    """
    JWT authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):

        try:
            # Close old database connections to prevent usage of timed out connections
            close_old_connections()

            user, jwt_value = JWTAuthenticationFromScope().authenticate(scope)
            scope['user'] = user
        except:
            scope['user'] = AnonymousUser()

        return self.inner(scope)