import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template
from core.models import UserMessage


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]  # Access user from the scope
        self.user_channel_name = f"user_{user.id}"
        async_to_sync(self.channel_layer.group_add)(self.user_channel_name, self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.user_channel_name, self.channel_name)

    def notification_message_func(self, event):
        user_message = UserMessage.objects.get(id=event['message_id'])
        user = user_message.user
        all_messages = UserMessage.objects.filter(user=user)
        # Only render messages for the connected user
        if user_message.user == self.scope["user"]:
            html = get_template('partials/message-list.html').render(
                context={'messages': all_messages}  # Show only the new message
            )
            self.send(text_data=html)
