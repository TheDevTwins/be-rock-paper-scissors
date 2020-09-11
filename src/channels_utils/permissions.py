class BasePermission:
    def has_permission(self, scope):
        return True

    def has_object_permission(self, scope, obj):
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, scope):
        return bool(scope['user'] and scope['user'].is_authenticated)


class IsInSession(BasePermission):
    def has_object_permisssion(self, scope, session):
        return bool(scope['user'] and session.players.filter(user=scope['user']))
