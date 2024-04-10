import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template
from core.models import UserMessage


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "notification-message"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.GROUP_NAME, self.channel_name)

    def notification_message_func(self, event):
        user_message = UserMessage.objects.get(id=event['message_id'])
        user = user_message.user
        all_messages = UserMessage.objects.filter(user=user)
        html = get_template('partials/message-list.html').render(
            context = {'messages': all_messages}
            )
        self.send(text_data=html)

