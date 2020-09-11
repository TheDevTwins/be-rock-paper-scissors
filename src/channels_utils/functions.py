from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_channels_group(channels_group_name, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(channels_group_name, event)
