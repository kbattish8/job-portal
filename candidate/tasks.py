from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chat.models import Notification  # your Notification model
from django.contrib.auth import get_user_model

User = get_user_model()
@shared_task
def send_application_notification(recipient_id, message, from_user_id=None):
    # Fetch recipient user (will raise User.DoesNotExist if invalid)
    recipient = User.objects.get(id=recipient_id)

    # Save notification in DB
    Notification.objects.create(
        recipient=recipient,
        message=message,
        type='job'  # or 'chat', 'system' depending on your use case
    )

    # Send WebSocket notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient_id}",
        {
            "type": "private_message",
            "message": message,
            "from_user": from_user_id
        }
    )
