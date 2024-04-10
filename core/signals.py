from core.models import UserMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=UserMessage)
def user_message_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # Get the user associated with the message
        user = instance.user

        # Create user-specific channel name
        channel_name = f"user_{user.id}"
        group_name = 'notification-message'
        event = {
            'type': 'notification_message_func',
            'message_id': instance.id
        }
        # Send message to the user's channel
        async_to_sync(channel_layer.group_send)(channel_name, event)