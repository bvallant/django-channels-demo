from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify(group_name, message, type='info', **extra):
    channel_layer = get_channel_layer()
    payload = {
        "message": message,
        "type": type,
        "date": timezone.now().isoformat(),
    }
    payload.update(extra)
    async_to_sync(channel_layer.group_send)(group_name, {"type": "notification", "payload": payload})
