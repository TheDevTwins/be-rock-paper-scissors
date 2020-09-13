from rest_framework import serializers

from .models import *


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = (
            'hat', 'face', 'skin', 'shirt'
        )


class PlayerSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Player
        fields = (
            'id', 'player_type', 'name', 'is_admin', 'avatar'
        )
