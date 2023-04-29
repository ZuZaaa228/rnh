import base64
import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from .models import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.client_id = self.scope["url_route"]["kwargs"]["appeal_id"]
        self.room_group_name = "chat_%s" % self.client_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        user = self.scope["user"]
        appeal = Appeal.objects.get(id=self.client_id)
        if user.is_authenticated and (user == appeal.author or user.is_admin):
            # User has permission to send message
            # async_to_sync(self.channel_layer.group_send)(
            #     self.room_group_name, {"type": "chat_message", "message": message}
            # )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": message, "sender": str(user),
                                       'datetime': str(timezone.now())}
            )
            message_save = Message(
                appeal=appeal,
                sender=user,
                text=message,
                time=timezone.now()
            )
            message_save.save()
        else:
            # User does not have permission to send message
            self.send(text_data=json.dumps({"error": "You are not authorized to send messages in this chat."}))

    # Receive message from room group
    # def chat_message(self, event):
    #     message = event["message"]
    #     # sender = event['sender']
    #
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         "message": message,
    #         # 'sender': sender,
    #     }))
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        time = datetime.now().strftime('%H:%M:%S')

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "time": time,
        }))
